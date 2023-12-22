import json
import mysql.connector
import datetime
import requests
from azure.cosmos import CosmosClient
import re
country_mapping = {
    "ru": "russe",
    "ir": "iranienne",
    "cn": "chinoise",
    "ua": "ukrainienne",
    "mx": "mexicaine",
    "sy": "syrienne",
    "co": "colombienne",
    "ae": "émiratie",
    "by": "biélorusse",
    "pk": "pakistanaise",
    "iq": "irakienne",
    "lb": "libanaise",
    "kp": "nord-coréenne",
    "cu": "cubaine",
    "af": "afghane",
    "tr": "turque",
    "gb": "britannique",
    "mm": "birmane",
    "hk": "hong-kongaise",
    "ve": "vénézuélienne",
    "cy": "chypriote",
    "us": "américaine",
    "de": "allemande",
    "ge": "géorgienne",
    "zw": "zimbabwéenne",
    "sg": "singapourienne",
    "az": "azerbaïdjanaise",
    "pa": "panaméenne",
    "cd": "congolaise",
    "my": "malaisienne",
    "ch": "suisse",
    "fr": "française",
    "it": "italienne",
    "ly": "libyenne",
    "bg": "bulgare",
    "th": "thaïlandaise",
    "ca": "canadienne",
    "ye": "yéménite",
    "so": "somalienne",
    "ps": "palestinienne",
    "za": "sud-africaine",
    "mt": "maltaise",
    "sa": "saoudienne",
    "es": "espagnole",
    "tn": "tunisienne",
    "pe": "péruvienne",
    "ni": "nicaraguayenne",
    "eg": "égyptienne",
    "na": "namibienne",
    "nl": "néerlandaise",
    "gt": "guatémaltèque",
    "ss": "sud-soudanaise",
    "in": "indienne",
    "rs": "serbe",
    "ba": "bosniaque",
    "be": "belge",
    "il": "israélienne",
    "mv": "maldivienne",
    "id": "indonésienne",
    "sd": "soudanaise",
    "ph": "philippine",
    "am": "arménienne",
    "hn": "hondurienne",
    "vg": "îles Vierges britanniques",
    "tw": "taïwanaise",
    "fi": "finlandaise",
    "cg": "congolaise",
    "jo": "jordanienne",
    "kw": "koweïtienne",
    "kz": "kazakhe",
    "cf": "centrafricaine",
    "ml": "malienne",
    "dz": "algérienne",
    "uz": "ouzbèke",
    "qa": "qatarienne",
    "kh": "cambodgienne",
    "xk": "kosovare",
    "jp": "japonaise",
    "su": "soviétique",
    "md": "moldave",
    "lv": "lettonne",
    "br": "brésilienne",
    "ke": "kényane",
    "gr": "grecque",
    "pl": "polonaise",
    "at": "autrichienne",
    "do": "dominicaine",
    "ng": "nigériane",
    "om": "omanaise",
    "py": "paraguayenne",
    "ee": "estonienne",
    "ug": "ougandaise",
    "kg": "kirghize",
    "ar": "argentine",
    "lr": "libérienne",
    "gm": "gambienne",
    "mh": "marshallaise",
    "ma": "marocaine",
    "ht": "haïtienne",
    "rw": "rwandaise",
    "lu": "luxembourgeoise",
    "ao": "angolaise",
    "bd": "bangladaise",
    "ms": "montserratienne",
    "cz": "tchèque",
    "vn": "vietnamienne",
    "sl": "sierra-léonaise",
    "ky": "caïmanaise",
    "se": "suédoise",
    "ie": "irlandaise",
    "ci": "ivoirienne",
    "sk": "slovaque",
    "lk": "srilankaise",
    "sv": "salvadorienne",
    "ec": "équatorienne",
    "gw": "guinéenne",
    "li": "liechtensteinoise",
    "si": "slovène",
    "bh": "bahreïnienne",
    "au": "australienne",
    "kn": "saint-kittsienne-et-nevicienne",
    "er": "érythréenne",
    "bz": "bélizienne",
    "bj": "béninoise",
    "sc": "seychelloise",
    "tz": "tanzanienne",
    "ro": "roumaine",
    "hu": "hongroise",
    "mz": "mozambicaine",
    "tj": "tadjike",
    "kr": "sud-coréenne",
    "jm": "jamaïcaine",
    "dj": "djiboutienne",
    "cl": "chilienne",
    "no": "norvégienne",
    "gn": "guinéenne",
    "et": "éthiopienne",
    "io": "britannique de l'océan Indien",
    "al": "albanaise",
    "hr": "croate",
    "me": "monténégrine",
    "je": "jersiaise",
    "gi": "gibraltarienne",
    "mc": "monégasque",
    "vc": "saint-vincentaise-et-grenadine",
    "bb": "barbadienne",
    "tg": "togolaise",
    "mk": "macédonienne du Nord",
    "tt": "trinidadienne",
    "tm": "turkmène",
    "dk": "danoise",
    "nz": "néo-zélandaise",
    "bf": "burkinabée",
    "bo": "bolivienne",
    "td": "tchadienne",
    "cr": "costaricienne",
    "mo": "macanaise",
    "cs": "yougoslave",
    "cw": "curaçao",
    "st": "santoméenne",
    "tv": "tuvaluane"
}

# Function to read the JSON data from a file

# Obtenez la date actuelle
aujourd_hui = datetime.date.today()

# Formatez la date actuelle comme "yyyyMMdd"
date_formattee = aujourd_hui.strftime("%Y%m%d")

# Génère l'URL de base
url_base = "https://data.opensanctions.org/datasets/"

# Concatène la base et la cible pour obtenir l'URL complète
url = url_base + date_formattee + "/sanctions/targets.nested.json"

#url = "https://data.opensanctions.org/datasets/20231005/sanctions/targets.nested.json"

# Chemin du fichier local où vous souhaitez enregistrer le JSON
destination = "C:/Users/rimba/Desktop/Tledger/api_sanctions/sanctions.json"

# Fonction pour télécharger le fichier JSON
def download_json(url, destination):
    response = requests.get(url)
    if response.status_code == 200:
        # Sauvegarde le contenu dans un fichier local
        with open(destination, 'wb') as file:
            file.write(response.content)
        return destination  # Retourne le chemin du fichier local
    else:
        return None
    
def read_json_from_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as json_file:
        for line in json_file:
            item = json.loads(line.strip())
            data.append(item)
    return data

# Function to insert or update data in Azure Cosmos DB
def update_cosmos_db(data, cosmos_client, database_name, container_name):
    database = cosmos_client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(id=container_name, partition_key="/id")

    for item in data:
        if item["schema"] == "Person":
            # Verify if the person already exists in the database
            #existing_person = container.read_item(item["id"], item["id"])
            i=1
            if i==2:
                # The person already exists; you can decide to update data here if needed
                pass
            else:
                # Check if nationality is an abbreviation, and replace it with the full name
                nationality = item["properties"].get("nationality", ["N/A"])[0].lower()
                if nationality in country_mapping:
                    nationality = country_mapping[nationality]

                # Convert the birthdate format from "YYYY-MM-DD" to "DD/MM/YYYY"
                birthdate_raw = item["properties"].get("birthDate", ["N/A"])[0]
                if re.match(r'\d{4}-\d{2}-\d{2}', birthdate_raw):
                    birthdate_obj = datetime.datetime.strptime(birthdate_raw, "%Y-%m-%d")
                    birthdate = birthdate_obj.strftime("%d/%m/%Y")
                else:
                    birthdate = birthdate_raw

                # Insert the new person into the database
                container.create_item(body={
                    'id': item["id"],
                    'name': item["caption"],
                    'names': ",".join(item["properties"].get("name", ["N/A"])),
                    'birthdate': birthdate,
                    'nationality': nationality
                })

def main():
    # Set your Cosmos DB URI and primary key
    cosmos_db_uri = "https://rim-database.documents.azure.com:443/"
    cosmos_db_key = "ap4Xg2ocAmRDetEmZUNsBqQ1jgIXWVWLQCN4HtLdVEJMLQK42A1XzWFRujsQEq6qMcv36gOaw2YkACDb2aUYTg=="

    # Instantiate the Cosmos DB client
    cosmos_client = CosmosClient(cosmos_db_uri, cosmos_db_key)

    # Path to the local JSON file where you have saved the data
    #local_json_path = download_json(url, destination)

    if destination:
        # Read the JSON data from the local file
        json_data = read_json_from_file(destination)

        if json_data:
            # Process the JSON data and extract relevant information
            sanctioned_people = []
            for item in json_data:
                if item["schema"] == "Person":
                    sanctioned_people.append(item)

            # Update Azure Cosmos DB with the extracted data
            update_cosmos_db(sanctioned_people, cosmos_client, "RimsDb", "Container1")

            print("Mise à jour terminée.")
        else:
            print("Impossible de lire le fichier JSON local.")
    else:
        print("Chemin invalide vers le fichier JSON local.")

if __name__ == "__main__":
    main()