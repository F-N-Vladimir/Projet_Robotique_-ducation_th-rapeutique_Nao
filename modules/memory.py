import json
import os
from datetime import datetime


class MemoryModule:
    DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

    def __init__(self, child_name):
        self.child_name = child_name
        os.makedirs(self.DATA_DIR, exist_ok=True)
        self.filepath = os.path.join(self.DATA_DIR, f"{child_name.lower()}.json")
        self.data = self._charger()

    def _charger(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "nom":               self.child_name,
            "nb_sessions":       0,
            "score_total":       0,
            "questions_total":   0,
            "erreurs_par_theme": {},
            "derniere_session":  None
        }

    def sauvegarder(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def enregistrer_session(self, theme, score, total, erreurs_themes):
        self.data["nb_sessions"]     += 1
        self.data["score_total"]     += score
        self.data["questions_total"] += total
        self.data["derniere_session"] = datetime.now().strftime("%d/%m/%Y")
        for t in erreurs_themes:
            self.data["erreurs_par_theme"][t] = (
                self.data["erreurs_par_theme"].get(t, 0) + 1
            )
        self.sauvegarder()

    def get_theme_difficile(self):
        erreurs = self.data["erreurs_par_theme"]
        if not erreurs:
            return None
        return max(erreurs, key=erreurs.get)

    def get_message_accueil(self):
        n      = self.data["nb_sessions"]
        prenom = self.child_name
        themes_fr = {
            "hypoglycemie": "l'hypoglycemie",
            "hyperglycemie": "l'hyperglycemie",
            "alimentation":  "l'alimentation",
            "insuline":      "l'insuline",
            "sport":         "le sport",
        }

        if n == 0:
            return (
                f"Bonjour {prenom} ! C'est ta premiere session avec moi. "
                "Je suis tres content de te rencontrer !"
            )

        score_moy = round(
            self.data["score_total"] /
            max(self.data["questions_total"], 1) * 100
        )
        msg = (
            f"Content de te revoir {prenom} ! "
            f"C'est ta session numero {n + 1}. "
            f"Ton score moyen est de {score_moy} pourcent. "
        )
        theme_dur = self.get_theme_difficile()
        if theme_dur:
            msg += (
                f"La derniere fois tu avais du mal avec "
                f"{themes_fr.get(theme_dur, theme_dur)}. "
                "On va retravailler ca ensemble !"
            )
        return msg

    def get_stats_dict(self):
        d     = self.data
        total = max(d["questions_total"], 1)
        return {
            "nom":             d["nom"],
            "nb_sessions":     d["nb_sessions"],
            "score_moyen":     round(d["score_total"] / total * 100),
            "theme_difficile": self.get_theme_difficile() or "aucun",
            "derniere_session": d["derniere_session"] or "jamais"
        }
