from modules.dialog import *
from modules.vision import identify_child
from modules.database import save_data
from modules.memory import MemoryModule
from modules.db_update import update_child_stats
import os


def main():
    introduction()

    say("Regarde-moi bien, je vais essayer de te reconnaitre.")
    nom_reconnu = identify_child()

    if nom_reconnu and nom_reconnu != "inconnu":
        say("Oh, je te reconnais ! Bonjour " + nom_reconnu)
        nom = nom_reconnu
        age = 8
        introduction(nom)
    else:
        say("Je ne te reconnais pas encore.")
        nom, age = get_basic_info()
        fichier_mem = os.path.join("data", nom.lower() + ".json")
        if os.path.exists(fichier_mem):
            say("Ah mais je connais ce prenom !")
            introduction(nom)
        else:
            say("Enchant de te rencontrer " + nom + " !")
            if os.path.exists("temp_capture.jpg"):
                os.rename("temp_capture.jpg", "faces/" + nom + ".jpg")
            save_data(nom, age, "", "", type_data="nouveau_profil")
            say("C est fait ! Je me souviendrai de toi " + nom)

    ask_feelings(nom, age)
    explain_diabetes()

    # ← NOUVEAU : choix du type de quiz
    say("Est-ce que tu veux faire un quiz rapide avec 3 questions, ou un quiz complet sur tous les themes ?")
    say("Dis rapide ou complet !")

    choix = listen()
    choix = choix.lower()

    if any(mot in choix for mot in ["complet", "tout", "long", "tous"]):
        say("Super ! On fait le quiz complet sur tous les themes !")
        score, total, nb_erreurs, theme = quiz_complet(nom, age)
    else:
        say("D accord ! On fait un quiz rapide avec 3 questions !")
        score, total, nb_erreurs, theme = quiz(nom, age, nombre=3)

    update_child_stats(nom, score, total, theme, nb_erreurs)
    say("Merci pour cette discussion ! A bientot !")


if __name__ == "__main__":
    main()