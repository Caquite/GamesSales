import mysql.connector

from mysql.connector import Error
import pandas as pd
import matplotlib.pyplot as plt


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
    except Error as e:
        print("Erreur connexion: " + str(e))
        return None

def analyse_uni_quali_nom2(table_principale, table_liaison,nom_colonne,nom_id):

    bdd = getBDD()
    if not bdd:
        return None
    
    try:
        query = """
        SELECT 
            p."""+nom_colonne+""" as """+nom_colonne+""", 
            COUNT(l.id_jeu) as Nb_Jeux
        FROM """ + table_principale + """ p
        LEFT JOIN """ + table_liaison + """ l ON p."""+nom_id+""" = l."""+nom_id+"""
        GROUP BY p."""+nom_id+""", p."""+nom_colonne+"""
        ORDER BY Nb_Jeux DESC
        """
        
        df=pd.read_sql_query(query,bdd)
        bdd.close()
        
        # Analyse
        print("Analyse univariée : Jeux par " +nom_colonne)
        print(df)
        print("Nombre total de "+nom_colonne+" : " + str(len(df)))
        print("Nombre total de jeux : " + str(df['Nb_Jeux'].sum()))
        
        # Graphique
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(df)), df['Nb_Jeux'],width=0.2, color='skyblue', edgecolor='navy')
        plt.title('Nombre de jeux par '+nom_colonne)
        plt.xlabel(nom_colonne)
        plt.ylabel('Nombre de jeux')
        plt.xticks(range(len(df)), df[nom_colonne], rotation=45, ha='right')
        
        # Nombres sur les barres
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    str(int(height)), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
        
        return df
        
    except Error as e:
        print("Erreur : " + str(e))
        return None

def analyse_uni_quali_nom(nom_table):
    
    bdd = getBDD()
    if not bdd:
        return None
    
    try:
        query = """ SELECT """+nom_table+""", COUNT(id_jeu) as Nb_Jeux FROM """+nom_table+""" GROUP BY """ + nom_table + """
        ORDER BY Nb_Jeux DESC
        LIMIT 20
        """
        
        df=pd.read_sql_query(query,bdd)
        bdd.close()
        
        # Analyse
        print("Analyse univariée : Jeux par " +nom_table)
        print(df)
        print("Nombre total de "+nom_table+" : " + str(len(df)))
        print("Nombre total de jeux : " + str(df['Nb_Jeux'].sum()))
        
        # Graphique
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(df)), df['Nb_Jeux'],width=0.3, color='skyblue', edgecolor='navy')
        plt.title('Nombre de jeux par '+nom_table)
        plt.xlabel(nom_table)
        plt.ylabel('Nombre de jeux')
        plt.xticks(range(len(df)), df[nom_table], rotation=45, ha='right')
        
        # Nombres sur les barres
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    str(int(height)), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
        
        return df
        
    except Error as e:
        print("Erreur : " + str(e))
        return None





analyse_uni_quali_nom2("categorie","a_categorie","categorie","id_cat")
analyse_uni_quali_nom2("os","a_os","OS","id_os")

analyse_uni_quali_nom("developpeur")
analyse_uni_quali_nom("genre")
analyse_uni_quali_nom("editeur")



#--------------------------Graphe qualitatif ordinal------------------

def analyse_uni_quali_ord(nom_table,nom_colonne):
    
    bdd = getBDD()
    if not bdd:
        return None
    
    try:
        query = """ SELECT """+nom_colonne+""", COUNT(id_jeu) as Nb_Jeux FROM """+nom_table+""" GROUP BY """+nom_colonne+"""
        ORDER BY """+nom_colonne+""" ASC
        LIMIT 20
        """
        
        df=pd.read_sql_query(query,bdd)
        bdd.close()
    

        # Analyse
        print("Analyse univariée : Jeux par " +nom_colonne)
        print(df)
        print(nom_colonne + str(len(df)))
        print("Nombre total de jeux : " + str(df['Nb_Jeux'].sum()))
        
        # Graphique
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(df)), df['Nb_Jeux'], width=1 ,color='skyblue', edgecolor='navy')
        plt.title('Nombre de jeux par '+nom_colonne)
        plt.xlabel(nom_colonne)
        plt.ylabel('Nombre de jeux')
        plt.xticks(range(len(df)), df[nom_colonne], rotation=45, ha='right')
        
        # Nombres sur les barres
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    str(int(height)), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
        
        return df
        
    except Error as e:
        print("Erreur : " + str(e))
        return None
analyse_uni_quali_ord('jeux','age_requis')
analyse_uni_quali_ord('jeux','annee')








