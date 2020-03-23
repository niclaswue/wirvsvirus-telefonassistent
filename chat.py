#!/usr/bin/python3
from io import BytesIO

import speech_recognition as sr
from gtts import gTTS
import pygame


# initialize pygame mixer for audio playback
pygame.mixer.init(28000)

# initialize speech recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()


def say(text):
    """Generate and play a sound file with the given text.

    Args:
        text (str): text to speech
    """
    if len(text) < 2:
        return
    tts = gTTS(text=text, lang='de')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(20)


def listen():
    """Record speech until silence is detected and return transkription.

    Returns:
        str: transcribed text from speech
    """
    try:
        with mic as source:
            print("Now recording, you can speak...")
            audio = r.listen(source, timeout=10.0)
        print("Recognizing...")
        text = r.recognize_google(audio, language="de-DE")
    except:
        # don't crash the program when speech recognition fails
        text = ""

    print("You said: {}".format(text))
    return text


def read_script_file(filename):
    """Read a script file containing the dialog.

    Args:
        filename (str): String or path to script file

    Returns:
        list: list of lines in script file
    """
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines


def analyse_answers(answers):
    """Analyse the answers given by the user.

    Args:
        answers (list): list of answers (1 = yes, 0 = no, -1 = no answer)

    Returns:
        str: Result of the analysis as text
    """
    threshold = 5

    # scores for each question
    # first element is the score for 'yes', second for 'no'
    scores = [(8, -1), (4, -1), (2, -1), (2, -1), (3, -2), (-2, 0),
              (3, -2), (-3, 0), (-2, 0), (-2, 0), (-2, 0)]

    score = 0

    # handle age question
    age = answers[0]
    if age < 40:
        score += -2
    elif age < 50:
        score += 0
    elif age < 60:
        score += 1
    elif age < 70:
        score += 2
    elif age < 80:
        score += 3
    else:
        score += 4

    # add up all the scores
    for i in range(1, len(answers)):
        ans = answers[i]
        if ans < 0:
            continue
        try:
            score += scores[i][ans]
        except:
            pass

    # classify whether patient has typical symptoms or not
    if score >= threshold:
        answer = """Sie leiden an einigen typischen Symptomen oder waren in 
        einem Risikogebiet! Sie können sich testen lassen, dazu wählen Sie 
        bitte folgende Nummer: 116117."""
    else:
        answer = """Sie haben nicht die typischen Symptome für den Coronavirus.
                  Bitte bleiben Sie zu Hause und meiden Sie den Kontakt mit anderen."""
    return answer


if __name__ == "__main__":
    script = read_script_file("chatscript.txt")

    answers = []

    # at the beginning adjust for ambient noise
    with mic as source:
        print("Adjusting microphone for ambient noise...")
        r.adjust_for_ambient_noise(source)
        r.dynamic_energy_threshold = False

    # read each sentence and listen for the response
    for sentence in script:
        print(sentence)
        # empty line inidcates listening
        listening = (sentence.strip() == "")
        number_of_trys = 3
        while listening and number_of_trys > 0:
            text = listen().lower()

            try:
                # try to cast answer to integer
                answers.append(int(text))
                break
            except:
                pass

            # detect yes, no or skip  as answer
            if "ja" in text:
                answers.append(1)
                break
            elif "nein" in text:
                answers.append(0)
                break
            elif "weiter" in text:
                answers.append(-1)
                break
            else:
                say("""Das habe ich leider nicht verstanden! Bitte wiederholen
                       Sie Ihre Antwort.""")
                number_of_trys -= 1
        else:
            if number_of_trys == 0:
                say("""Ok, das habe ich leider auch nicht verstanden. Wir 
                       machen mit der nächsten Frage weiter.""")
        say(sentence)

    # analyse and speak result
    result = analyse_answers(answers)
    say(result)
    say("Vielen Dank für Ihren Anruf! Bleiben Sie gesund.")
