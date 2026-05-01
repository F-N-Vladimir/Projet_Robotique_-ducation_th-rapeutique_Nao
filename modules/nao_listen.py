import sys
sys.path.append("/opt/pynaoqi/lib/python2.7/site-packages")

from naoqi import ALProxy
import time

IP = "11.0.0.135"
PORT = 9559

asr = ALProxy("ALSpeechRecognition", IP, PORT)
memory = ALProxy("ALMemory", IP, PORT)

asr.setLanguage("French")

vocabulaire = ["A", "B", "C"]
asr.setVocabulary(vocabulaire, False)

asr.subscribe("Test_ASR")

print("ECOUTE...")

time.sleep(5)

data = memory.getData("WordRecognized")

asr.unsubscribe("Test_ASR")

print(data)
