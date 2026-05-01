from modules.dialog import *
from modules.vision import identify_child
from modules.database import save_data
from modules.memory import MemoryModule
from modules.db_update import update_child_stats
from modules.jeu_cuisinier import jeu_cuisinier
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

    # Choix de l'activite
    say("Qu est-ce que tu veux faire aujourd hui ?")
    say("Dis QUIZ pour repondre a des questions, ou JEU pour jouer au jeu du chef cuisinier !")

    choix_activite = listen().lower()

    if any(m in choix_activite for m in ["jeu", "cuisin", "chef", "manger", "aliment"]):
        say("Super ! On joue au jeu du chef cuisinier !")
        jeu_cuisinier(nom, age, nb_manches=5)

        # Apres le jeu, proposer un quiz rapide
        say("Maintenant tu veux faire un petit quiz rapide pour finir ?")
        reponse = listen().lower()
        if any(m in reponse for m in ["oui", "ok", "bien", "sur", "ouais", "allez"]):
            score, total, nb_erreurs, theme = quiz(nom, age, nombre=3)
            update_child_stats(nom, score, total, theme, nb_erreurs)
        else:
            say("D accord, on s arrete la pour aujourd hui !")

    else:
        # Quiz normal
        say("Est-ce que tu veux un quiz rapide avec 3 questions, ou un quiz complet ?")
        say("Dis rapide ou complet !")
        choix_quiz = listen().lower()

        if any(m in choix_quiz for m in ["complet", "tout", "long", "tous"]):
            say("Super ! On fait le quiz complet !")
            score, total, nb_erreurs, theme = quiz_complet(nom, age)
        else:
            say("D accord ! Quiz rapide avec 3 questions !")
            score, total, nb_erreurs, theme = quiz(nom, age, nombre=3)

        update_child_stats(nom, score, total, theme, nb_erreurs)

    say("Merci pour cette session ! Tu as tres bien travaille. A bientot !")


if __name__ == "__main__":
    main()
