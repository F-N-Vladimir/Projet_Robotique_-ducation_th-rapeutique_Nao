import cv2
import os

class ALTextToSpeech:
    def say(self, text):
        print(f"NAO: {text}")

class ALSpeechRecognition:
    def setLanguage(self, lang): pass
    def setVocabulary(self, vocab, enable): pass
    def subscribe(self, name): pass
    def unsubscribe(self, name): pass

class ALMemory:
    def subscriber(self, event): return self
    def getData(self, key): return None
    def signal(self): return self
    def connect(self, callback): pass

class ALAnimatedSpeech:
    def say(self, text):
        clean = text.replace("^start(", "").replace("^wait(", "")
        for part in clean.split(")"):
            part = part.strip()
            if part:
                print(f"NAO: {part}")

class ALVideoDevice:
    def __init__(self):
        print("[SIMULATION] Connexion au module robot : ALVideoDevice")

class qi:
    @staticmethod
    def Session():
        return None
