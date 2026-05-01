# Projet_Robotique_-ducation_th-rapeutique_Nao

#  Robot NAO — Education Therapeutique Diabete Type 1

Projet de 2eme annee de Licence Informatique.

Systeme robotique base sur le robot humanoide NAO pour aider les enfants
atteints du diabete de type 1 a apprendre a gerer leur maladie.

---

## Fonctionnalites

- Reconnaissance faciale avec suivi de visage (ALTracker + face_recognition)
- Interaction 100% vocale (micro NAO + Google Speech Recognition)
- Quiz adaptatif sur 5 themes medicaux (16 questions)
- Jeu du chef cuisinier (20 aliments bons/mauvais)
- Memoire persistante inter-sessions (JSON + MySQL)
- Mouvements du robot (salutation, approbation, au revoir)

---

## Technologies

- Python 3 (logique applicative)
- Python 2.7 (SDK NaoQi — communication robot)
- PHP + MySQL (API backend)
- OpenCV + face_recognition (vision)
- SpeechRecognition + Google Speech (voix)
- XAMPP (serveur web local)

---

## Prerequis

### Materiel
- Robot NAO (SoftBank Robotics) — optionnel, simulation possible
- PC sous Ubuntu Linux
- Webcam (si pas de robot)

### Logiciels
```bash
# Python 3
sudo apt-get install python3 python3-pip

# Python 2.7 + SDK NaoQi
sudo apt-get install python2.7
# Telecharger le SDK NaoQi depuis SoftBank Robotics
# Placer dans /opt/pynaoqi/

# Bibliotheques Python 3
pip3 install face_recognition opencv-python SpeechRecognition numpy requests

# Bibliotheques systeme
sudo apt-get install python3-pyaudio portaudio19-dev

# Serveur web
# Installer XAMPP depuis https://www.apachefriends.org/
```

---

## Installation

### 1. Cloner le projet
```bash
git clone https://github.com/TON_USERNAME/nao_diabetes_project.git
cd nao_diabetes_project
```

### 2. Configurer la base de donnees
```bash
# Demarrer XAMPP
sudo /opt/lampp/lampp start

# Creer la base de donnees
/opt/lampp/bin/mysql -u root < sql/structure.sql
```

### 3. Configurer l'API
```bash
# Copier et editer le fichier de configuration
cp api/config_db.example.php api/config_db.php
nano api/config_db.php
# Modifier DB_NAME, DB_USER, DB_PASS selon votre configuration
```

### 4. Configurer l'IP du robot
```bash
nano config.py
# Modifier ROBOT_IP avec l'IP de votre robot NAO
# Exemple : ROBOT_IP = "11.0.0.135"
```

### 5. Creer les dossiers necessaires
```bash
mkdir -p data faces
```

---

## Utilisation

### Lancer le programme principal
```bash
python3 main.py
```

### Voir la camera NAO en direct
```bash
./camera_nao
```

### Tester la reconnaissance faciale seule
```bash
python3 - << 'PYEOF'
from modules.vision import identify_child
print(identify_child())
PYEOF
```

### Tester la voix du robot
```bash
python2.7 - << 'PYEOF'
import sys
sys.path.insert(0, '/opt/pynaoqi/lib/python2.7/site-packages')
from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "11.x.x.x", 9559)
tts.setLanguage("French")
tts.say("Bonjour !")
PYEOF
```

---

## Structure du Projet


nao_diabetes_project/
├── main.py                  # Point d'entree principal
├── config.py                # Configuration (IP robot, URLs API)
├── naoqi.py                 # Mock simulation NAO sur PC
├── nao_face_tracker.py      # Suivi de visage Python 2.7
├── nao_listen.py            # Reconnaissance vocale NAO Python 2.7
├── nao_mouvement.py         # Mouvements du robot
├── camera_nao               # Script pour voir la camera en direct
│
├── modules/
│   ├── vision.py            # Reconnaissance faciale
│   ├── speech.py            # Voix et micro
│   ├── dialog.py            # Quiz et dialogue
│   ├── memory.py            # Memoire persistante JSON
│   ├── questions.py         # Base de 16 questions
│   ├── database.py          # Client API PHP
│   ├── db_update.py         # Mise a jour stats MySQL
│   └── jeu_cuisinier.py     # Jeu des aliments
│
├── api/
│   ├── config_db.example.php  # Template configuration BD
│   ├── save_data.php          # Sauvegarde interactions
│   ├── update_stats.php       # Mise a jour statistiques
│   └── get_memory.php         # Lecture profil enfant
│
├── sql/
│   ├── structure.sql          # Schema complet base de donnees
│   └── memory_update.sql      # Colonnes statistiques
│
├── data/                    # Profils JSON (gitignore)
├── faces/                   # Images biometriques (gitignore)
└── docs/
├── rapport.docx           # Rapport de projet
└── presentation.pptx      # Diaporama de presentation



---

## Mode Simulation (sans robot)

Le projet fonctionne sans robot physique grace au module mock :

```bash
# Le fichier naoqi.py simule le robot automatiquement
# Si le robot n'est pas accessible, le systeme bascule sur :
# - Webcam PC pour la reconnaissance faciale
# - Micro PC + Google Speech pour la reconnaissance vocale
python3 main.py
```

---

## Auteur

**Vladimir** — 2eme Annee Licence Informatique — 2025-2026

Inspire des projets europeens ALIZ-E (FP7) et PAL (H2020).

---

## References

- Blanson Henkemans et al. (2017) — PAL Project
- ALIZ-E Project — FP7 European Commission
- SoftBank Robotics — NAO Documentation
