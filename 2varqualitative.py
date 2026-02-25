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
    # If the user asks for 'genre', join jeux -> genre on id_jeu
    'genre': "jeux JOIN genre ON jeux.id_jeu = genre.id_jeu",
    
    # If the user asks for 'editeur', join jeux -> editeur
    'editeur': "jeux JOIN editeur ON jeux.id_jeu = editeur.id_jeu",
    
    # If the user asks for 'developpeur', join jeux -> developpeur
    'developpeur': "jeux JOIN developpeur ON jeux.id_jeu = developpeur.id_jeu",
    
    # 'os' is special: it needs to go through 'a_os'
    'os': "jeux JOIN a_os ON jeux.id_jeu = a_os.id_jeu JOIN os ON a_os.id_os = os.id_os",
    
    # 'categorie' is special: it needs to go through 'a_categorie'
    'categorie': "jeux JOIN a_categorie ON jeux.id_jeu = a_categorie.id_jeu JOIN categorie ON a_categorie.id_cat = categorie.id_cat"
}

def plot_smart_relationship(col_x, table_x, col_y, table_y):
    connect = getBDD()
    if not connect: return

    #si les deux tables sont 'jeux'
    if table_x == 'jeux' and table_y == 'jeux':
        sql_from = "jeux"
    else:
        #si une des deux tables est 'jeux', on prend l'autre comme cible pour trouver le chemin de jointure
        target_table = table_x if table_x != 'jeux' else table_y
        
        #chercher le chemin de jointure dans RELATIONSHIPS
        if target_table in RELATIONSHIPS:
            sql_from = RELATIONSHIPS[target_table]
        else:
            print(f"Error: Can't join to table '{target_table}' .")
            return
        
    sql = f"SELECT {table_x}.{col_x}, {table_y}.{col_y} FROM {sql_from}"
    
    print(f"Generating SQL: {sql}")
    df = pd.read_sql(sql, connect)
    connect.close()

    #nettoyage : si une colonne est du texte mais ressemble à un nombre, essayons de la convertir pour les graphiques
    for col in [col_x, col_y]:
        if df[col].dtype == 'object':
            # Try to convert to float if it looks like a number
            try:
                df[col] = df[col].str.replace(',', '.').astype(float)
            except:
                pass

    plt.figure(figsize=(12, 6))

    # Verifier les types de données pour choisir le bon graphique
    x_is_number = df[col_x].dtype != 'object'
    y_is_number = df[col_y].dtype != 'object'
    
    # Les 2 sont des nombres-> Scatter Plot
    if x_is_number and y_is_number:
        sns.scatterplot(data=df, x=col_x, y=col_y, alpha=0.5)
        plt.title(f'Scatter Plot: {col_x} vs {col_y}')

    # 1 texte et 1 nombre -> Bar Plot
    elif y_is_number: 
        avg_data = df.groupby(col_x)[col_y].mean().sort_values(ascending=False).head(10)
        sns.barplot(x=avg_data.index, y=avg_data.values, palette='viridis')
        plt.title(f'Top 10 {col_x} by Average {col_y}')
        plt.xticks(rotation=45)

    # 2 textes -> Heatmap
    else:
        ct = pd.crosstab(df[col_x], df[col_y])
        sns.heatmap(ct, annot=True, fmt='d', cmap='Blues')
        plt.title(f'Heatmap: {col_x} vs {col_y}')

    plt.tight_layout()
    plt.show()

#test
plot_smart_relationship('genre', 'genre', 'annee', 'jeux')