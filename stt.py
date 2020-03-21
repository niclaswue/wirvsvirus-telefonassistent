#!/Users/bach/workspace/default/default_env/bin/python3
import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
    print("Adjusting microphone for ambient noise...")
    r.adjust_for_ambient_noise(source)
    print("Now recording, you can speak...")
    audio = r.listen(source)

print("Recognizing...")
text = r.recognize_google(audio, language="de-DE")
print("You said: {}".format(text))
