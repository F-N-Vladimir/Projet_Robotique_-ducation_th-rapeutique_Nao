import face_recognition
import os

FACES_DIR = "faces"

def charger_visages():
    encodings = []
    noms = []

    for file in os.listdir(FACES_DIR):
        if file.endswith(".jpg"):
            path = os.path.join(FACES_DIR, file)
            image = face_recognition.load_image_file(path)

            face_enc = face_recognition.face_encodings(image)

            if face_enc:
                encodings.append(face_enc[0])
                noms.append(os.path.splitext(file)[0])

    return encodings, noms


def reconnaitre_visage(image_path):
    known_encodings, known_names = charger_visages()

    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)

    if not encodings:
        return "inconnu"

    for face in encodings:
        results = face_recognition.compare_faces(known_encodings, face)

        if True in results:
            index = results.index(True)
            return known_names[index]

    return "inconnu"
