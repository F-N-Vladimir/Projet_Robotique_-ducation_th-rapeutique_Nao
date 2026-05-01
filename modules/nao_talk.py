import sys
sys.path.append("/opt/pynaoqi/lib/python2.7/site-packages")

from naoqi import ALProxy

IP = "11.0.0.135"
PORT = 9559

animated = ALProxy("ALAnimatedSpeech", IP, PORT)

text = sys.argv[1]

animated.say("^start(animations/Stand/Gestures/Explain_1) " + text)
