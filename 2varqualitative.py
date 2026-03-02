import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def getBDD():
    try:
        bdd = mysql.connector.connect(
            host='localhost',
            database='gamesale',
            user='root',
            password='',
            charset='utf8'
        )
        return bdd
    except Exception as e:
        print("Connection Error: " + str(e))
        return None
    
# Les cles etrangères & les chemins de jointure pour les relations communes
RELATIONSHIPS = {
    'genre': "jeux JOIN genre ON jeux.id_jeu = genre.id_jeu",
    'editeur': "jeux JOIN editeur ON jeux.id_jeu = editeur.id_jeu",
    'developpeur': "jeux JOIN developpeur ON jeux.id_jeu = developpeur.id_jeu",
    'os': "jeux JOIN a_os ON jeux.id_jeu = a_os.id_jeu JOIN os ON a_os.id_os = os.id_os",
    'categorie': "jeux JOIN a_categorie ON jeux.id_jeu = a_categorie.id_jeu JOIN categorie ON a_categorie.id_cat = categorie.id_cat"
}

def plot_smart_relationship(col_x, table_x, col_y, table_y):
    connect = getBDD()
    if not connect: return

    needed_joins = []
    if table_x != 'jeux' and table_x in RELATIONSHIPS:
        needed_joins.append(RELATIONSHIPS[table_x].replace("jeux ", ""))
    if table_y != 'jeux' and table_y in RELATIONSHIPS and table_y != table_x:
        needed_joins.append(RELATIONSHIPS[table_y].replace("jeux ", ""))

    sql_from = f"jeux {' '.join(needed_joins)}"
    sql = f"SELECT {table_x}.{col_x}, {table_y}.{col_y} FROM {sql_from}"
    
    print(f"🚀 Executing: {sql}")
    df = pd.read_sql(sql, connect)
    connect.close()

    df[col_x] = df[col_x].astype(str)
    df[col_y] = df[col_y].astype(str)

    ct = pd.crosstab(df[col_x], df[col_y])

    plt.figure(figsize=(14, 10))
    
    sns.heatmap(ct, annot=True, fmt='d', cmap="YlGnBu", cbar_kws={'label': 'Frequency'})

    plt.title(f'Heatmap Analysis: {col_x} vs {col_y}', fontsize=15)
    plt.xlabel(col_y)
    plt.ylabel(col_x)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

#test
plot_smart_relationship('genre', 'genre', 'developpeur', 'developpeur')