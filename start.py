import sys
import speech_recognition as sr
print(sys.version)
print(sr.__version__)
r = sr.Recognizer()
sr.Microphone.list_microphone_names()

#mic = sr.Microphone(device_index=3)

# with mic as source:

#with harvard as source:
#    audio = r.record(source)

# r.recognize_google(audio)