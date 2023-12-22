import requests

def check_sanction(nom, prenom, date_naissance, nationalite):
    data = {
        "nom": nom,
        "prenom": prenom,
        "date_naissance": date_naissance,
        "nationalite": nationalite
    }

    # Envoyer la requête à l'API
    api_url = "https://sanctionsapp.azurewebsites.net/search"
    response = requests.post(api_url, json=data)

    if response.status_code == 200:
        result = response.json()
        if result['message'] == "Sanction correspondante trouvée de cet utilisateur.":
            return 1 
        elif result['message'] == "Pas de sanction.":
            return "0"  
        elif result['message'] == "Personne mineure.":
            return "2"  
        else:
            return None  
    else:
        return None  