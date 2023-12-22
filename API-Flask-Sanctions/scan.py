import mysql.connector

# Informations de connexion à la base de données des utilisateurs
user_db_config = {
    "host": "node15210-tledgerdb.my.p4d.click",
    "user": "tunicash",
    "password": "5NWWKP1oZrHo7.0c",
    "database": "tunicash",
    "port": 11007,
}

# Informations de connexion à la base de données des sanctions
sanction_db_config = {
    "host": "10.30.2.189",
    "user": "root",
    "password": "4eG21kWFZ9",
    "database": "sanctions",
}

# Établir une connexion aux bases de données
user_db = mysql.connector.connect(**user_db_config)
sanction_db = mysql.connector.connect(**sanction_db_config)

# Créer des curseurs pour les bases de données
user_cursor = user_db.cursor()
sanction_cursor = sanction_db.cursor()

# Récupérer toutes les lignes de la table "users"
user_cursor.execute("SELECT id, fname, lname FROM users")
users = user_cursor.fetchall()

# Récupérer toutes les valeurs de la colonne "name" de la table "sanction"
sanction_cursor.execute("SELECT name FROM sanction")
sanction_names = [name[0] for name in sanction_cursor.fetchall()]

# Liste pour stocker les personnes sanctionnées
sanctioned_users = []

# Parcourir les utilisateurs et chercher des correspondances
for user in users:
    full_name = user[1] + " " + user[2]
    if full_name in sanction_names:
        #print(f"Correspondance trouvée pour : {full_name}")
        # Ajouter les informations de la personne sanctionnée à la liste
        sanctioned_users.append(user)

tunicash_cursor = user_db.cursor()
# Insérer les personnes sanctionnées dans la table "sanctioned_users"
for user in sanctioned_users:
    id, fname, lname = user
    insert_query = "INSERT INTO sanctioned_users (id, prenom, nom) VALUES (%s, %s, %s)"
    values = (id, fname, lname)
    tunicash_cursor.execute(insert_query, values)
    
    update_query = "UPDATE users SET flaged = 1 WHERE id = %s"
    tunicash_cursor.execute(update_query, (id,))

# Committer les modifications dans la base de données des sanctions
user_db.commit()

# Fermer les connexions et curseurs
user_cursor.close()
user_db.close()
sanction_cursor.close()
sanction_db.close()
