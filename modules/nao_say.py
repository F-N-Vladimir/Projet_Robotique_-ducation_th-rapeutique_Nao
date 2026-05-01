# nao_say.py
import sys
sys.path.append("/opt/pynaoqi/lib/python2.7/site-packages")

from naoqi import ALProxy

IP = "11.0.0.135"
PORT = 9559

tts = ALProxy("ALTextToSpeech", IP, PORT)
tts.setLanguage("French")

text = sys.argv[1]
tts.say(text)
