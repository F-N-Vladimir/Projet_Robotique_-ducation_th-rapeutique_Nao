import requests

API_URL = "http://localhost/nao_diabetes_project/api/save_data.php"


def save_data(nom, age, question, reponse, type_data="interaction"):
    try:
        payload = {
            "nom":       nom,
            "age":       age,
            "question":  question,
            "reponse":   reponse,
            "type_data": type_data
        }
        response = requests.post(API_URL, json=payload, timeout=5)
        print(f"[DEBUG SQL] Envoi reussi : {response.status_code}")
    except Exception as e:
        print(f"[ERREUR] save_data : {e}")
