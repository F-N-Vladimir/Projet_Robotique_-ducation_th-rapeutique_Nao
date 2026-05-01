from modules.speech import say, listen
from modules.database import save_data
import random


# Base de donnees des aliments
ALIMENTS = {
    "bons": [
        {"nom": "les lentilles",      "raison": "Elles ont un index glycemique bas et liberent le sucre lentement."},
        {"nom": "le pain complet",    "raison": "Il contient des fibres qui ralentissent l'absorption du sucre."},
        {"nom": "les brocolis",       "raison": "Les legumes verts sont excellents, ils contiennent tres peu de sucre."},
        {"nom": "les oeufs",          "raison": "Les oeufs ne contiennent pas de glucides, parfait pour les diabetiques."},
        {"nom": "le poulet grille",   "raison": "Les proteines n'affectent pas la glycemie."},
        {"nom": "les amandes",        "raison": "Les oleagineux ont un IG tres bas et sont riches en bons nutriments."},
        {"nom": "le yaourt nature",   "raison": "Sans sucre ajoute, il est bien tolere par les diabetiques."},
        {"nom": "les carottes",       "raison": "Crues, elles ont un IG modere et sont riches en vitamines."},
        {"nom": "le poisson",         "raison": "Les proteines et omega 3 du poisson sont excellents pour la sante."},
        {"nom": "les fraises",        "raison": "Ce sont des fruits peu sucres et riches en vitamines."},
    ],
    "mauvais": [
        {"nom": "le soda",            "raison": "Il contient enormement de sucre rapide qui fait monter la glycemie tres vite."},
        {"nom": "les bonbons",        "raison": "Ce sont des sucres rapides qui font monter la glycemie tres vite."},
        {"nom": "le pain blanc",      "raison": "Son index glycemique est tres eleve, il fait monter le sucre rapidement."},
        {"nom": "les frites",         "raison": "Tres riches en glucides rapides et en graisses, a eviter."},
        {"nom": "le gateau au chocolat", "raison": "Plein de sucre et de graisses, il fait beaucoup monter la glycemie."},
        {"nom": "le jus de fruit",    "raison": "Meme naturel, il contient beaucoup de sucre rapide sans les fibres du fruit."},
        {"nom": "les cereales sucrees","raison": "Elles sont souvent tres riches en sucres caches."},
        {"nom": "la confiture",       "raison": "Elle est composee principalement de sucre, a consommer avec grande moderation."},
        {"nom": "les chips",          "raison": "Riches en glucides et en graisses, elles font monter la glycemie."},
        {"nom": "la limonade",        "raison": "Comme le soda, elle est pleine de sucres rapides."},
    ]
}


def extraire_choix(texte):
    """Extrait bon ou mauvais de la reponse vocale."""
    texte = texte.lower()
    if any(m in texte for m in ["bon", "bonne", "bien", "sain", "oui", "mange", "correct"]):
        return "bon"
    if any(m in texte for m in ["mauvais", "mauvaise", "non", "evite", "pas bon", "interdit", "danger"]):
        return "mauvais"
    return None


def jeu_cuisinier(nom, age, nb_manches=5):
    """
    Jeu du chef cuisinier :
    NAO presente un aliment, l'enfant dit si c'est bon ou mauvais pour un diabetique.
    """
    say(f"On va jouer au jeu du chef cuisinier {nom} !")
    say("Je vais te nommer des aliments.")
    say("Tu dois me dire si c est BON ou MAUVAIS pour un enfant diabetique.")
    say("Pret ? C est parti !")

    score     = 0
    mauvaises = []

    # Melanger et selectionner les aliments
    bons     = random.sample(ALIMENTS["bons"],    min(nb_manches // 2 + 1, len(ALIMENTS["bons"])))
    mauvais  = random.sample(ALIMENTS["mauvais"], min(nb_manches // 2, len(ALIMENTS["mauvais"])))
    selection = bons + mauvais
    random.shuffle(selection)
    selection = selection[:nb_manches]

    for i, aliment in enumerate(selection):
        nom_aliment = aliment["nom"]

        # Determiner si c'est bon ou mauvais
        est_bon = aliment in [a for a in ALIMENTS["bons"] if a["nom"] == nom_aliment]
        bonne_reponse = "bon" if est_bon else "mauvais"

        say(f"Aliment numero {i + 1} : {nom_aliment}.")
        say("C est bon ou mauvais pour toi ?")

        # Ecouter la reponse avec 2 essais
        reponse_enfant = None
        for essai in range(2):
            reponse_brute  = listen()
            reponse_enfant = extraire_choix(reponse_brute)

            if reponse_enfant:
                break
            if essai == 0:
                say("Je n ai pas bien compris. Dis bon ou mauvais !")

        # Si toujours pas compris apres 2 essais
        if not reponse_enfant:
            say(f"Je n ai pas compris. La bonne reponse etait : {bonne_reponse} !")
            say(aliment["raison"])
            mauvaises.append(nom_aliment)
            save_data(nom, age, f"Cuisinier: {nom_aliment}", "non_compris", type_data="jeu")
            continue

        # Verifier la reponse
        if reponse_enfant == bonne_reponse:
            score += 1
            if bonne_reponse == "bon":
                say(f"Bravo {nom} ! C est bien un bon aliment !")
            else:
                say(f"Excellent {nom} ! C est bien a eviter !")
            say(aliment["raison"])
        else:
            if bonne_reponse == "bon":
                say(f"Pas tout a fait {nom}. En fait {nom_aliment} est BON pour toi !")
            else:
                say(f"Attention {nom} ! {nom_aliment} est MAUVAIS pour toi !")
            say(aliment["raison"])
            mauvaises.append(nom_aliment)

        save_data(nom, age, f"Cuisinier: {nom_aliment}", reponse_enfant, type_data="jeu")

    # Bilan final
    say(f"Jeu termine {nom} ! Tu as eu {score} bonnes reponses sur {nb_manches}.")

    if score == nb_manches:
        say("Parfait ! Tu es un vrai chef cuisinier diabetique ! Tu sais exactement quoi manger !")
    elif score >= nb_manches // 2:
        say("Bien joue ! Tu connais bien les aliments. Continue comme ca !")
    else:
        say("Ne t inquiete pas ! On va apprendre ensemble quels aliments sont bons pour toi.")

    if mauvaises:
        say("Les aliments sur lesquels tu dois faire attention sont :")
        for aliment in mauvaises:
            say(aliment)

    return score, nb_manches
