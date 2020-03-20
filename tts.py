#!/Users/bach/workspace/default/default_env/bin/python3
from gtts import gTTS
import sys

args = sys.argv
text = args[1]
tts = gTTS(text, lang="de")

file_name = args[2]
tts.save(file_name)