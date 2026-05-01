import random

QUESTIONS = {
    "hypoglycemie": [
        {
            "question": "Hypoglycemie veut dire ?",
            "options": ["A : Trop de sucre", "B : Pas assez de sucre", "C : Trop de sel"],
            "correct": "B",
            "explication": "Hypoglycemie = glycemie trop basse, moins de 0.70 g/L.",
            "theme": "hypoglycemie"
        },
        {
            "question": "Quel est le premier signe d'une hypoglycemie ?",
            "options": ["A : Fievre", "B : Tremblements et sueurs", "C : Toux"],
            "correct": "B",
            "explication": "Les tremblements et sueurs sont les premiers signaux d'alarme.",
            "theme": "hypoglycemie"
        },
        {
            "question": "Que fais-tu en cas d'hypoglycemie ?",
            "options": ["A : Tu dors", "B : Tu fais du sport", "C : Tu manges du sucre rapide"],
            "correct": "C",
            "explication": "Il faut du sucre rapide : jus de fruit, bonbon ou sucre.",
            "theme": "hypoglycemie"
        },
        {
            "question": "A partir de quelle valeur parle-t-on d'hypoglycemie ?",
            "options": ["A : 0.50 g/L", "B : 0.70 g/L", "C : 1.20 g/L"],
            "correct": "B",
            "explication": "En dessous de 0.70 g/L, c'est une hypoglycemie.",
            "theme": "hypoglycemie"
        },
    ],
    "hyperglycemie": [
        {
            "question": "Hyperglycemie veut dire ?",
            "options": ["A : Trop de sucre dans le sang", "B : Pas assez de sucre", "C : Manque de sel"],
            "correct": "A",
            "explication": "Hyperglycemie = trop de sucre dans le sang, au-dessus de 1.80 g/L.",
            "theme": "hyperglycemie"
        },
        {
            "question": "Quel signe montre une hyperglycemie ?",
            "options": ["A : Tremblements", "B : Grande soif et fatigue", "C : Toux"],
            "correct": "B",
            "explication": "La grande soif, la fatigue et les mictions frequentes sont les signes.",
            "theme": "hyperglycemie"
        },
        {
            "question": "Que peut causer une hyperglycemie repetee ?",
            "options": ["A : Rien de grave", "B : Des problemes aux yeux et aux reins", "C : Un rhume"],
            "correct": "B",
            "explication": "A long terme, l'hyperglycemie abime les vaisseaux sanguins.",
            "theme": "hyperglycemie"
        },
    ],
    "alimentation": [
        {
            "question": "Quel aliment a un index glycemique tres eleve ?",
            "options": ["A : Lentilles", "B : Pain blanc", "C : Fromage"],
            "correct": "B",
            "explication": "Le pain blanc est digere vite et fait monter la glycemie rapidement.",
            "theme": "alimentation"
        },
        {
            "question": "Les lentilles ont un index glycemique ?",
            "options": ["A : Tres eleve", "B : Moyen", "C : Bas"],
            "correct": "C",
            "explication": "Les lentilles ont un IG bas, elles liberent le sucre lentement.",
            "theme": "alimentation"
        },
        {
            "question": "Que contiennent souvent les sodas ?",
            "options": ["A : Des vitamines", "B : Beaucoup de sucres caches", "C : Du calcium"],
            "correct": "B",
            "explication": "Un soda peut contenir jusqu'a 7 morceaux de sucre !",
            "theme": "alimentation"
        },
        {
            "question": "Quel pain est meilleur pour un diabetique ?",
            "options": ["A : Pain blanc", "B : Pain de mie", "C : Pain complet"],
            "correct": "C",
            "explication": "Le pain complet a un IG plus bas grace aux fibres.",
            "theme": "alimentation"
        },
    ],
    "insuline": [
        {
            "question": "A quoi sert l'insuline ?",
            "options": [
                "A : Digerer les graisses",
                "B : Faire entrer le glucose dans les cellules",
                "C : Filtrer le sang"
            ],
            "correct": "B",
            "explication": "L'insuline est comme une cle qui ouvre les cellules pour le glucose.",
            "theme": "insuline"
        },
        {
            "question": "Dans le diabete de type 1, le pancreas ?",
            "options": [
                "A : Produit trop d'insuline",
                "B : Ne produit plus d'insuline",
                "C : Fonctionne normalement"
            ],
            "correct": "B",
            "explication": "Dans le DT1, les cellules beta sont detruites. Il faut injecter l'insuline.",
            "theme": "insuline"
        },
        {
            "question": "Comment s'appelle l'organe qui produit l'insuline ?",
            "options": ["A : Le foie", "B : Le pancreas", "C : Le rein"],
            "correct": "B",
            "explication": "C'est le pancreas qui produit normalement l'insuline.",
            "theme": "insuline"
        },
    ],
    "sport": [
        {
            "question": "Que fait le sport sur la glycemie ?",
            "options": ["A : Elle monte", "B : Elle descend", "C : Elle ne change pas"],
            "correct": "B",
            "explication": "Le sport consomme du glucose, donc la glycemie descend pendant l'effort.",
            "theme": "sport"
        },
        {
            "question": "Avant le sport, tu dois ?",
            "options": [
                "A : Injecter plus d'insuline",
                "B : Verifier ta glycemie et manger si besoin",
                "C : Rien faire"
            ],
            "correct": "B",
            "explication": "Il faut toujours verifier sa glycemie avant le sport pour eviter l'hypo.",
            "theme": "sport"
        },
        {
            "question": "Pendant le sport, si tu te sens faible, tu dois ?",
            "options": ["A : Continuer", "B : Dormir", "C : Prendre du sucre et t'arreter"],
            "correct": "C",
            "explication": "Si tu te sens faible pendant le sport, c'est peut-etre une hypo !",
            "theme": "sport"
        },
    ],
}


def get_questions_aleatoires(theme, nombre=3):
    questions = QUESTIONS.get(theme, [])
    return random.sample(questions, min(nombre, len(questions)))


def get_tous_themes():
    return list(QUESTIONS.keys())
