import speech_recognition as sr
from gtts import gTTS
import pygame
from io import BytesIO

r = sr.Recognizer()
mic = sr.Microphone()

#pygame.init()
pygame.mixer.init(28000)


def say(text):
    if len(text) < 2:
        return
    tts = gTTS(text=text, lang='de')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(20)

def listen():
    try:
        with mic as source:
            print("Now recording, you can speak...")
            audio = r.listen(source, timeout=10.0)
        
        print("Recognizing...")
        text = r.recognize_google(audio, language="de-DE")
    except Exception as e:
        print(e)
        text = ""


    print("You said: {}".format(text))
    return text

def read_script_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines

def analyse_answers(answers):
    threshold = 5

    score = 0
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

    scores = [(8, -1), (4, -1), (2, -1), (2, -1), (3, -2), (-2, 0), (3, -2), (-3, 0), (-2, 0), (-2, 0), (-2, 0)]

    for i in range(1, len(answers)):
        ans = answers[i]
        if ans < 0:
            continue
        try:
            score += scores[i][ans]
        except Exception as e:
            pass
    
    if score >= threshold:
        return "Sie leiden an einigen typischen Symptomen oder waren in einem Risikogebiet! Sie können sich testen lassen, dazu wählen Sie bitte folgende Nummer: 116117."
    else:
        return "Sie haben nicht die typischen Symptome für den Coronavirus. Bitte bleiben Sie zu Hause und meiden Sie den Kontakt mit anderen."


if __name__ == "__main__":    
    script = read_script_file("chatscript.txt")
        
    answers = []

    with mic as source:
        print("Adjusting microphone for ambient noise...")
        r.adjust_for_ambient_noise(source)
        r.dynamic_energy_threshold = False

    for sentence in script:
        print(sentence)
        listening = (sentence.strip() == "")
        number_of_trys = 3
        while listening and number_of_trys > 0:
            text = listen().lower()

            try:
                answers.append(int(text))
                break
            except:
                pass

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
                say("Das habe ich leider nicht verstanden! Können Sie das nochmal wiederholen?")
                number_of_trys -= 1
        else:
            if number_of_trys == 0:
                say("Ok, das habe ich leider auch nicht verstanden. Wir machen mit der nächsten Frage weiter.")
        say(sentence)
    result = analyse_answers(answers)
    say(result)
    say("Vielen Dank für Ihren Anruf! Bleiben Sie gesund.")