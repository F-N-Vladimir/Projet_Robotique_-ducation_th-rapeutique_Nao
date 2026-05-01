import subprocess
import speech_recognition as sr
import os
import sys

sys.stderr = open(os.devnull, 'w')

ROBOT_IP   = "11.0.0.135"
ROBOT_PORT = 9559
NAO_LISTEN_SCRIPT = os.path.join(
    os.path.dirname(__file__), "..", "nao_listen.py"
)

def _nao_disponible():
    import socket
    try:
        s = socket.create_connection((ROBOT_IP, ROBOT_PORT), timeout=2)
        s.close()
        return True
    except:
        return False

NAO_CONNECTE = _nao_disponible()
if NAO_CONNECTE:
    print("[NAO] Robot connecte !")
else:
    print("[NAO] Robot non accessible — mode simulation")


def say(text):
    """Fait parler le NAO."""
    print("NAO: " + text)
    if not NAO_CONNECTE:
        return
    text_safe = text.replace("'", " ").replace('"', ' ')
    script = """import sys
sys.path.insert(0, '/opt/pynaoqi/lib/python2.7/site-packages')
from naoqi import ALProxy
try:
    tts = ALProxy("ALTextToSpeech", "%s", %d)
    tts.setLanguage("French")
    tts.say('%s')
except:
    pass
""" % (ROBOT_IP, ROBOT_PORT, text_safe)
    try:
        subprocess.run(
            ["python2.7", "-c", script],
            timeout=15,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL
        )
    except:
        pass


def listen(nb_essais=2):
    """
    Si NAO connecte : utilise le micro du robot.
    Sinon : utilise le micro du PC.
    """
    if NAO_CONNECTE:
        return _ecouter_nao()
    else:
        return _ecouter_pc(nb_essais)


def _ecouter_nao():
    """Ecoute via le micro du robot NAO."""
    print("[MICRO NAO] Ecoute en cours...")
    try:
        result = subprocess.run(
            ["python2.7", NAO_LISTEN_SCRIPT],
            capture_output=True,
            text=True,
            timeout=15
        )
        output = result.stdout.strip()
        print("[DEBUG NAO Listen] " + output)

        for ligne in output.split("\n"):
            if ligne.startswith("RECONNU:"):
                texte = ligne.replace("RECONNU:", "").strip()
                print("Enfant (NAO micro) : " + texte)
                return texte

        print("[MICRO NAO] Pas compris → micro PC")
        return _ecouter_pc(1)

    except subprocess.TimeoutExpired:
        print("[MICRO NAO] Timeout → micro PC")
        return _ecouter_pc(1)
    except Exception as e:
        print("[MICRO NAO] Erreur : " + str(e))
        return _ecouter_pc(1)


def _ecouter_pc(nb_essais=2):
    """Ecoute via le micro du PC — fallback."""
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold          = 1.2

    old_stderr = sys.stderr
    sys.stderr  = open(os.devnull, 'w')

    for essai in range(1, nb_essais + 1):
        try:
            with sr.Microphone() as source:
                sys.stderr = old_stderr
                if essai == 1:
                    print("[MICRO PC] Calibration...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                else:
                    print("[MICRO PC] Nouvel essai (%d/%d)..." % (essai, nb_essais))
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)

                print("[MICRO PC] Parle maintenant...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
                print("[MICRO PC] Reconnaissance...")

                texte = recognizer.recognize_google(audio, language="fr-FR")
                print("Enfant (vocal) : " + texte)
                return texte

        except sr.WaitTimeoutError:
            sys.stderr = old_stderr
            print("[MICRO PC] Timeout (essai %d/%d)" % (essai, nb_essais))
        except sr.UnknownValueError:
            sys.stderr = old_stderr
            print("[MICRO PC] Non compris (essai %d/%d)" % (essai, nb_essais))
        except sr.RequestError:
            sys.stderr = old_stderr
            print("[MICRO PC] Pas internet → clavier")
            return _clavier()
        except Exception as e:
            sys.stderr = old_stderr
            print("[MICRO PC] Erreur : " + str(e))
            return _clavier()
        finally:
            sys.stderr = old_stderr

    return _clavier()


def _clavier():
    """Fallback clavier."""
    print("[FALLBACK] Tape ta reponse :")
    return input("Enfant (clavier): ")
