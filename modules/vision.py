import os
import subprocess
import face_recognition
import numpy as np
import time

os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.*=false"
os.environ["QT_QPA_PLATFORM"]  = "xcb"
import cv2

ROBOT_IP   = "11.0.0.135"
ROBOT_PORT = 9559
FACES_DIR  = os.path.join(os.path.dirname(__file__), "..", "faces")
TEMP_IMAGE = os.path.join(os.path.dirname(__file__), "..", "temp_capture.jpg")


def _charger_visages_connus():
    encodages, noms = [], []
    if not os.path.exists(FACES_DIR):
        os.makedirs(FACES_DIR)
        return encodages, noms
    for fichier in os.listdir(FACES_DIR):
        if fichier.lower().endswith((".jpg", ".jpeg", ".png")):
            chemin = os.path.join(FACES_DIR, fichier)
            image  = face_recognition.load_image_file(chemin)
            enc    = face_recognition.face_encodings(image)
            if enc:
                encodages.append(enc[0])
                noms.append(os.path.splitext(fichier)[0])
    return encodages, noms


def _script_flux_nao():
    """Script Python 2.7 qui capture les frames NAO en RGB et les sauvegarde."""
    return """import sys, os, time, struct
sys.path.insert(0, '/opt/pynaoqi/lib/python2.7/site-packages')
from naoqi import ALProxy

ROBOT_IP   = "{ip}"
ROBOT_PORT = {port}
FRAME_FILE = "/tmp/nao_frame.bin"
META_FILE  = "/tmp/nao_meta.txt"

try:
    video  = ALProxy("ALVideoDevice", ROBOT_IP, ROBOT_PORT)
    cam_id = video.subscribeCamera("nao_stream", 0, 2, 11, 15)
    print("CAM_OK")
    sys.stdout.flush()

    while True:
        image = video.getImageRemote(cam_id)
        if image and image[6]:
            w, h = image[0], image[1]
            with open(FRAME_FILE, "wb") as f:
                f.write(image[6])
            with open(META_FILE, "w") as f:
                f.write(str(w) + "," + str(h))
            print("FRAME_OK")
            sys.stdout.flush()
        time.sleep(0.08)

except Exception as e:
    print("CAM_ERROR: " + str(e))
    sys.stdout.flush()
finally:
    try:
        video.unsubscribe(cam_id)
    except:
        pass
""".format(ip=ROBOT_IP, port=ROBOT_PORT)


def _lire_frame_nao():
    """Lit la derniere frame NAO depuis les fichiers temporaires."""
    frame_file = "/tmp/nao_frame.bin"
    meta_file  = "/tmp/nao_meta.txt"

    if not os.path.exists(frame_file) or not os.path.exists(meta_file):
        return None

    try:
        with open(meta_file, "r") as f:
            w, h = map(int, f.read().strip().split(","))

        with open(frame_file, "rb") as f:
            data = f.read()

        arr = np.frombuffer(data, dtype=np.uint8)

        if len(arr) == w * h * 3:
            img = arr.reshape((h, w, 3))
            return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return None

    except Exception:
        return None


def capturer_visage():
    """
    Utilise le suivi de visage NAO :
    - Le robot tourne la tete pour suivre le visage
    - Attend 3 secondes de stabilite
    - Capture automatiquement
    Fallback sur webcam PC si NAO inaccessible.
    """
    print("\n[CAMERA] Activation du suivi de visage NAO...")

    script_path = os.path.join(
        os.path.dirname(__file__), "..", "nao_face_tracker.py"
    )

    try:
        result = subprocess.run(
            ["python2.7", script_path],
            capture_output=True,
            text=True,
            timeout=20
        )

        output = result.stdout
        print("[NAO Tracker]", output.strip())

        # Verifier si la capture a reussi
        if "CAPTURE_OK" in output:
            # Convertir l'image RGB en JPEG lisible
            img_path = "/tmp/nao_face_capture.jpg"
            meta_path = "/tmp/nao_meta.txt"

            if os.path.exists(meta_path):
                with open(meta_path) as f:
                    w, h = map(int, f.read().strip().split(","))

                with open(img_path, "rb") as f:
                    data = f.read()

                arr = __import__('numpy').frombuffer(data, dtype=__import__('numpy').uint8)

                if len(arr) == w * h * 3:
                    img = arr.reshape((h, w, 3))
                    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(TEMP_IMAGE, img_bgr)
                    print("[CAMERA] Photo capturee via suivi NAO !")
                    return True

        if "ERREUR_CONNEXION" in output:
            print("[CAMERA] NAO non accessible → webcam PC")
            return _capturer_webcam_pc()

    except subprocess.TimeoutExpired:
        print("[CAMERA] Timeout → webcam PC")
    except Exception as e:
        print(f"[CAMERA] Erreur : {e} → webcam PC")

    return _capturer_webcam_pc()

def _capturer_webcam_pc():
    """Fallback webcam PC — capture avec ESPACE, detection allégée."""
    print("[CAMERA] Webcam PC — Appuie sur ESPACE pour capturer")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERREUR] Aucune camera disponible")
        return False

    cv2.namedWindow("Webcam PC — Appuie sur ESPACE", cv2.WINDOW_NORMAL)

    captured   = False
    compteur   = 0
    locations  = []   # derniere detection connue

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()
        compteur += 1

        # Detection toutes les 10 frames seulement (allege le CPU)
        if compteur % 10 == 0:
            small  = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb    = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
            locs   = face_recognition.face_locations(rgb)
            # Remettre a l'echelle x2
            locations = [(t*2, r*2, b*2, l*2) for (t, r, b, l) in locs]

        # Dessiner les rectangles avec la derniere detection connue
        for (top, right, bottom, left) in locations:
            cv2.rectangle(display, (left, top), (right, bottom), (0, 220, 0), 2)

        # Instructions a l'ecran
        if locations:
            cv2.putText(display, "Visage detecte — ESPACE pour capturer",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 220, 0), 2)
        else:
            cv2.putText(display, "Placez-vous face a la camera",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.putText(display, "ESPACE = capturer | ECHAP = annuler",
                    (10, display.shape[0] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow("Webcam PC — Appuie sur ESPACE", display)

        # waitKey court = interface reactive
        key = cv2.waitKey(1) & 0xFF

        if key == 32:   # ESPACE — capture immediate sans attendre visage
            cv2.imwrite(TEMP_IMAGE, frame)
            print("[CAMERA] Photo capturee !")
            captured = True
            break
        elif key == 27:  # ECHAP
            print("[CAMERA] Annule")
            break

    cap.release()
    cv2.destroyAllWindows()
    return captured


def identify_child():
    """Capture le visage et identifie l'enfant."""
    captured = capturer_visage()

    if not captured or not os.path.exists(TEMP_IMAGE):
        print("[ANALYSE] Echec de la capture")
        return "inconnu"

    print("[ANALYSE] Reconnaissance faciale en cours...")

    image_inconnue     = face_recognition.load_image_file(TEMP_IMAGE)
    encodages_inconnus = face_recognition.face_encodings(image_inconnue)

    if not encodages_inconnus:
        print("[ANALYSE] Aucun visage dans la photo")
        return "inconnu"

    encodage_inconnu              = encodages_inconnus[0]
    encodages_connus, noms_connus = _charger_visages_connus()

    if not encodages_connus:
        print("[ANALYSE] Aucun visage enregistre dans faces/")
        return "inconnu"

    distances = face_recognition.face_distance(encodages_connus, encodage_inconnu)
    index_min = np.argmin(distances)

    if distances[index_min] < 0.5:
        nom = noms_connus[index_min]
        print(f"[ANALYSE] Reconnu : {nom} (similarite : {1 - distances[index_min]:.1%})")
        return nom

    print(f"[ANALYSE] Non reconnu (similarite max : {1 - distances[index_min]:.1%})")
    return "inconnu"