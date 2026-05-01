from modules.speech import say, listen
from modules.database import save_data
from modules.memory import MemoryModule
from modules.questions import get_questions_aleatoires, get_tous_themes


def ask(nom, age, question):
    say(question)
    reponse = listen()
    save_data(nom, age, question, reponse, type_data="interaction")
    return reponse


def extraire_lettre(texte):
    """
    Extrait A, B ou C d'une phrase vocale.
    Gere : 'reponse B', 'le B', 'B', 'deuxieme', 'deux', etc.
    """
    texte = texte.upper().strip()

    # Cherche A, B ou C comme mot isole
    for lettre in ["A", "B", "C"]:
        if texte == lettre:
            return lettre
        if f" {lettre} " in f" {texte} ":
            return lettre
        if texte.endswith(f" {lettre}"):
            return lettre
        if texte.startswith(f"{lettre} "):
            return lettre

    # Cherche par position ordinale
    if any(m in texte for m in ["PREMIER", "PREMIERE", "UN ", "UNE ", "1"]):
        return "A"
    if any(m in texte for m in ["DEUXIEME", "DEUX", "2"]):
        return "B"
    if any(m in texte for m in ["TROISIEME", "TROIS", "3"]):
        return "C"

    # Cherche par contenu partiel (ex: "pas assez" → B)
    if any(m in texte for m in ["PAS ASSEZ", "MANQUE", "INSUFFI"]):
        return "B"
    if any(m in texte for m in ["TROP DE SUCRE", "BEAUCOUP"]):
        return "A"

    return texte  # retourne tel quel si rien trouve


def introduction(nom=""):
    if nom:
        mem = MemoryModule(nom)
        message = mem.get_message_accueil()
        say(message)
    else:
        say("Bonjour mon ami ! Je suis le robot NAO.")
        say("Je vais discuter avec toi et t'aider a apprendre sur le diabète .")


def get_basic_info():
    reponse_nom = ask("", "", "Comment tu t'appelles ?")
    nom = reponse_nom.strip().split()[-1].capitalize()
    reponse_age = ask(nom, "", "Quel age as-tu ?")
    age = next((m for m in reponse_age.split() if m.isdigit()), "8")
    return nom, age


def ask_feelings(nom, age):
    ask(nom, age, "Comment tu te sens aujourd'hui ?")


def explain_diabetes():
    say("Le diabete est une maladie ou le sucre dans le sang n'est pas bien controle.")
    say("L'insuline aide le sucre a entrer dans le corps.")


def quiz_complet(nom, age):
    """Quiz complet sur tous les themes."""
    mem = MemoryModule(nom)

    themes = [
        "hypoglycemie",
        "hyperglycemie",
        "alimentation",
        "insuline",
        "sport"
    ]

    score          = 0
    nb_erreurs     = 0
    total          = 0
    erreurs_themes = []

    for theme in themes:
        questions = get_questions_aleatoires(theme, 100)
        say(f"On commence le theme {theme.replace('_', ' ')}")

        for i, q in enumerate(questions):
            total += 1
            say(f"Question {total} : {q['question']}")
            for option in q["options"]:
                say(option)

            reponse = ask(nom, age, "Quelle est ta reponse ?")
            lettre  = extraire_lettre(reponse)

            if lettre == q["correct"].upper():
                say("Bravo !")
                score += 1
            else:
                say(f"Pas tout a fait. La bonne reponse etait {q['correct']}.")
                say(q["explication"])
                nb_erreurs += 1
                erreurs_themes.append(theme)

    say(f"Quiz termine ! Tu as obtenu {score} bonnes reponses sur {total}.")

    if score == total:
        say(f"Parfait {nom} ! Score parfait, tu es un champion !")
    elif score >= total // 2:
        say(f"Bien joue {nom} ! Continue comme ca !")
    else:
        say(f"Ne t inquiete pas {nom}, on va retravailler ca ensemble !")

    mem.enregistrer_session("global", score, total, erreurs_themes)
    return score, total, nb_erreurs, "global"


def quiz(nom, age, theme=None, nombre=3):
    """Quiz rapide sur un theme specifique."""
    mem = MemoryModule(nom)

    if theme is None:
        theme_difficile = mem.get_theme_difficile()
        theme = theme_difficile if theme_difficile else "hypoglycemie"

    questions      = get_questions_aleatoires(theme, nombre)
    score          = 0
    nb_erreurs     = 0
    erreurs_themes = []

    say(f"On va faire un quiz sur {theme.replace('_', ' ')} avec {len(questions)} questions !")

    for i, q in enumerate(questions):
        say(f"Question {i + 1} : {q['question']}")
        for option in q["options"]:
            say(option)

        reponse = ask(nom, age, "Quelle est ta reponse ?")
        lettre  = extraire_lettre(reponse)

        if lettre == q["correct"].upper():
            say("Bravo ! C'est la bonne reponse !")
            score += 1
        else:
            say(f"Pas tout a fait. La bonne reponse etait {q['correct']}.")
            say(f"Explication : {q['explication']}")
            nb_erreurs += 1
            erreurs_themes.append(theme)

    total = len(questions)
    say(f"Quiz termine ! Tu as eu {score} bonne reponse sur {total}.")

    if score == total:
        say(f"Parfait {nom} ! Score parfait, tu es un champion !")
    elif score >= total // 2:
        say(f"Bien joue {nom} ! Continue comme ca !")
    else:
        say(f"Ne t inquiete pas {nom}, on va retravailler ca ensemble !")

    mem.enregistrer_session(theme, score, total, erreurs_themes)
    return score, total, nb_erreurs, theme


def role_play(nom, age):
    mem = MemoryModule(nom)
    answer = ask(nom, age, "Tu te sens faible, que fais-tu ? Prendre du sucre ou dormir ?")

    if "sucre" in answer.lower():
        say("Tres bien !")
        mem.enregistrer_session("sport", score=1, total=1, erreurs_themes=[])
    else:
        say("Attention, il faut prendre du sucre rapidement !")
        mem.enregistrer_session("sport", score=0, total=1, erreurs_themes=["sport"])
