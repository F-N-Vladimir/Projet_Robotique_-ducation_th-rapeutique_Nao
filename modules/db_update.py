import requests
from datetime import datetime

UPDATE_URL = "http://localhost/nao_diabetes_project/api/update_stats.php"


def update_child_stats(nom, score_quiz, total_questions, theme, nb_erreurs):
    try:
        payload = {
            "nom":             nom,
            "score_quiz":      score_quiz,
            "total_questions": total_questions,
            "theme":           theme,
            "nb_erreurs":      nb_erreurs,
            "date":            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        response = requests.post(UPDATE_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"[INFO] Stats MySQL mises a jour pour {nom}")
        else:
            print(f"[ERREUR] update_stats.php : {response.status_code}")
    except Exception as e:
        print(f"[ERREUR] update_child_stats : {e}")
