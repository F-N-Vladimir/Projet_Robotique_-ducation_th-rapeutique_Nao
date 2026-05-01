# -*- coding: utf-8 -*-
import sys
import time

sys.path.insert(0, '/opt/pynaoqi/lib/python2.7/site-packages')
from naoqi import ALProxy

ROBOT_IP   = "11.0.0.135"
ROBOT_PORT = 9559

def main():
    try:
        tts    = ALProxy("ALTextToSpeech",      ROBOT_IP, ROBOT_PORT)
        asr    = ALProxy("ALSpeechRecognition", ROBOT_IP, ROBOT_PORT)
        memory = ALProxy("ALMemory",            ROBOT_IP, ROBOT_PORT)

        # Arreter proprement avant de configurer
        try:
            asr.unsubscribe("NAO_Listen")
        except:
            pass

        asr.pause(True)

        vocabulaire = [
            "A", "B", "C",
            "oui", "non",
            "bon", "mauvais",
            "rapide", "complet",
            "quiz", "jeu",
            "bien", "mal",
	    "je m'appelle", "je me sens bien",
	    "je suis un peu fatiguer",
        ]

        asr.setLanguage("French")
        asr.setVocabulary(vocabulaire, False)
        asr.pause(False)

        # IMPORTANT : effacer l'ancienne valeur avant d'ecouter
        memory.insertData("WordRecognized", [])

        asr.subscribe("NAO_Listen")
        print("ECOUTE_OK")
        sys.stdout.flush()

        # Attendre une reponse max 12 secondes
        debut = time.time()
        while time.time() - debut < 12:
            try:
                resultat = memory.getData("WordRecognized")
                if resultat and len(resultat) >= 2 and resultat[0]:
                    mot       = str(resultat[0]).strip()
                    confiance = float(resultat[1])
                    print("DEBUG: mot=[%s] confiance=%.2f" % (mot, confiance))
                    sys.stdout.flush()
                    if confiance > 0.25 and mot:
                        print("RECONNU:" + mot)
                        sys.stdout.flush()
                        break
            except:
                pass
            time.sleep(0.2)
        else:
            print("TIMEOUT")

        asr.unsubscribe("NAO_Listen")

    except Exception as e:
        print("ERREUR:" + str(e))

if __name__ == "__main__":
    main()
