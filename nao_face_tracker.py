# -*- coding: utf-8 -*-
import sys
import os
import time

sys.path.insert(0, '/opt/pynaoqi/lib/python2.7/site-packages')
from naoqi import ALProxy

ROBOT_IP        = "11.0.0.135"
ROBOT_PORT      = 9559
OUTPUT_IMG      = "/tmp/nao_face_capture.jpg"
STABLE_SECONDES = 3


def main():
    print("[NAO] Connexion au robot...")

    try:
        tts     = ALProxy("ALTextToSpeech", ROBOT_IP, ROBOT_PORT)
        video   = ALProxy("ALVideoDevice",  ROBOT_IP, ROBOT_PORT)
        tracker = ALProxy("ALTracker",      ROBOT_IP, ROBOT_PORT)
        motion  = ALProxy("ALMotion",       ROBOT_IP, ROBOT_PORT)
        posture = ALProxy("ALRobotPosture", ROBOT_IP, ROBOT_PORT)
        print("[NAO] Connexion reussie !")

    except Exception as e:
        print("ERREUR_CONNEXION: " + str(e))
        sys.exit(1)

    try:
        # 1. Mettre le robot en position stable
        motion.wakeUp()

        # 2. Message d'accueil
        tts.setLanguage("French")
        tts.say("Bonjour ! Regarde moi et fais moi un signe de la main !")

        # 3. Activer le suivi de visage
        print("[NAO] Activation du suivi de visage...")
        tracker.registerTarget("Face", 0.1)
        tracker.setMode("Head")
        tracker.track("Face")
        print("[NAO] Suivi actif - le robot suit ton visage")

        tts.say("Je te vois ! Reste bien face a moi.")

        # 4. Attendre stabilisation
        print("[NAO] Attente %d secondes..." % STABLE_SECONDES)
        time.sleep(STABLE_SECONDES)

        # 5. Capturer
        print("[NAO] Capture de l image...")
        tts.say("Souris !")
        time.sleep(0.5)

        cam_id = video.subscribeCamera("face_capture", 0, 2, 11, 15)
        time.sleep(0.3)
        image = video.getImageRemote(cam_id)
        video.unsubscribe(cam_id)

        if image and image[6]:
            w = image[0]
            h = image[1]
            with open(OUTPUT_IMG, "wb") as f:
                f.write(image[6])
            with open("/tmp/nao_meta.txt", "w") as f:
                f.write(str(w) + "," + str(h))
            print("CAPTURE_OK:" + OUTPUT_IMG)
            tts.say("Super ! J ai pris ta photo !")
        else:
            print("CAPTURE_ERREUR: image vide")

    except Exception as e:
        print("ERREUR: " + str(e))

    finally:
        try:
            tracker.stopTracker()
            tracker.unregisterAllTargets()
            print("[NAO] Suivi desactive")
        except:
            pass


if __name__ == "__main__":
    main()
