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

def analyse_uni_quanti_dis(nom_table,nom_colonne):
    
    bdd = getBDD()
    if not bdd:
        return None
    
    try:
        query = """ SELECT 
        CASE 
            WHEN """+nom_colonne+"""<50 THEN '0-49'
            WHEN """+nom_colonne+"""<100 THEN '50-99'
            WHEN """+nom_colonne+"""<150 THEN '100-149'
            WHEN """+nom_colonne+"""<200 THEN '150-199'
            WHEN """+nom_colonne+"""<250 THEN '200-249'
            WHEN """+nom_colonne+"""<300 THEN '250-299'
            WHEN """+nom_colonne+"""<350 THEN '300-349'
            WHEN """+nom_colonne+"""<400 THEN '350-399'
            WHEN """+nom_colonne+"""<450 THEN '400-449'
            WHEN """+nom_colonne+"""<500 THEN '450-499'
            WHEN """+nom_colonne+"""<550 THEN '500-549'
            WHEN """+nom_colonne+"""<600 THEN '550-599'
            ELSE '600+'
        END AS classe, COUNT(id_jeu) as Nb_Jeux FROM """+nom_table+"""
        GROUP BY classe
        ORDER BY FIELD(classe, '0-49', '50-99', '100-149', '150-199', '200-249', '250-299', '300-349', '350-399','400-449', '450-499','500-549', '550-599', '600+')
        """
        
        df=pd.read_sql_query(query,bdd)
        bdd.close()
    

        # Analyse
        print("Analyse univariée quantitative discrète : Jeux par " +nom_colonne)
        print(df)
        print(nom_colonne + str(len(df)))
        print("Nombre total de jeux : " + str(df['Nb_Jeux'].sum()))
        
        # Graphique
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(df)), df['Nb_Jeux'], width=0.3 ,color='skyblue', edgecolor='navy')
        plt.title('Nombre de jeux par '+nom_colonne)
        plt.xlabel(nom_colonne)
        plt.ylabel('Nombre de jeux')
        plt.xticks(range(len(df)), df['classe'], rotation=45, ha='right')
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
analyse_uni_quanti_dis('jeux','nb_succes')
analyse_uni_quanti_dis('jeux','nb_avis_pos')
analyse_uni_quanti_dis('jeux','nb_avis_neg')
analyse_uni_quanti_dis('jeux','temps_jeu_moyen')










