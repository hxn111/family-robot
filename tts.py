import sys
from robot_hat import TTS

text_to_say = "Hi, its time to brush your teeth. Are you ready?"
tts = TTS(lang="en-US")
tts.say(text_to_say)