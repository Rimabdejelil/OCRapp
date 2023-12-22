from flask import Flask, request, jsonify
from azure.cosmos import CosmosClient
from datetime import datetime
import re

app = Flask(__name__)

# Cosmos DB Configuration
cosmos_db_uri = "https://rim-database.documents.azure.com:443/"
cosmos_db_key = "fQiwUvjeaZDJt7i7d76W9AcrESCoL9S1cUkXN3rBYz5ZNtgzLpf14VAGO6VGBOvhFhIYnpz37f8BACDbeXRpWQ=="
cosmos_client = CosmosClient(cosmos_db_uri, cosmos_db_key)
database_name = "RimsDb"
container_name = "Container1"

# Select the database
database = cosmos_client.get_database_client(database_name)

# Select the container
container = database.get_container_client(container_name)

# Function to perform the search in Cosmos DB
def search_sanctions(nom, prenom, date_naissance, nationalite):
    # Ensure that the name and surname are not empty
    if not nom.strip() or not prenom.strip():
        return None

    # Combine the first name and last name with a space in the middle
    nom_complet = prenom + ' ' + nom

    # Calculate age from the date of birth
    pattern = re.compile(r'\d{2}/\d{2}/\d{4}')

    # Check if the date matches the format
    if pattern.match(date_naissance):
        birthdate = datetime.strptime(date_naissance, '%d/%m/%Y')
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        # Check if the person is a minor
        if age < 18:
            return "Mineur"

    # Query to search for matches in Cosmos DB
    query = (
        f"SELECT * FROM c "
        f"WHERE c.name = '{nom_complet}' "
        f"AND c.birthdate = '{date_naissance}' "
        f"AND c.nationality = '{nationalite}'"
    )

    # Execute the query
    results = list(container.query_items(query, enable_cross_partition_query=True))

    # Return the result
    return results

# Endpoint to perform the search
@app.route('/search', methods=['POST'])
def perform_search():
    data = request.json

    nom = data.get('nom', '')
    prenom = data.get('prenom', '')
    date_naissance = data.get('date_naissance', '')
    nationalite = data.get('nationalite', '')

    result = search_sanctions(nom, prenom, date_naissance, nationalite)

    if result == "Mineur":
        return jsonify({'message': 'Personne mineure.'}), 200
    elif result:
        return jsonify({'message': 'Sanction correspondante trouvée de cet utilisateur.'}), 200
    else:
        return jsonify({'message': 'Pas de sanction.'}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)