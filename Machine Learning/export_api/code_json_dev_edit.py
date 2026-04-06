import mysql.connector
import json
import pandas as pd

# Connexion à la BDD
connexion = mysql.connector.connect(
    host='localhost', user='root', password='', database='gamesale'
)


# -----------------------------------
# Ici on va créer deux fichiers JSON dans le but de faire le lien entre les noms
# d'éditeur et de développeur, et leurs identifiants numériques, car pour les modèles
# il nous faut des entiers pour les champs id_developpeur et id_editeur.
# Seul façon d'obtenir le bon identifiant sans avoir accès a notre BDD est d'utiliser
# un JSON dans lequel tout est noté


# Éditeurs
df_edit = pd.read_sql("SELECT id_editeur, editeur FROM editeur GROUP BY id_editeur", connexion)
editeurs = dict(zip(df_edit['editeur'], df_edit['id_editeur']))
with open('editeurs.json', 'w', encoding='utf-8') as f:
    json.dump(editeurs, f, ensure_ascii=False)

# Développeurs
df_dev = pd.read_sql("SELECT id_developpeur, developpeur FROM developpeur GROUP BY id_developpeur", connexion)
developpeurs = dict(zip(df_dev['developpeur'], df_dev['id_developpeur']))
with open('developpeurs.json', 'w', encoding='utf-8') as f:
    json.dump(developpeurs, f, ensure_ascii=False)

connexion.close()