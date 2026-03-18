# %%
import numpy as np
import pandas as pd
from scipy import stats
import importlib

import mysql.connector
from mysql.connector import Error
import warnings
warnings.filterwarnings("ignore")

if importlib.util.find_spec("sklearn") is None:
    import subprocess
    subprocess.run(["pip", "install", "scikit-learn"])

from sklearn.linear_model import LinearRegression



## Importation données
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
    
bdd = getBDD()



## Algo de regression (rappel)
def droite_regression(df, var1, var2):
    """
    Création d'un scatter plot et d'une droite de regression pour visualiser les données.
    Arguments :
        df : data frame 
        var1 : variable pour l'axe x
        var2 : variable pour l'axe y
        ax : emplacement du graphe si on fait du multi affichage
        titre : chaine de carractère pour le titre du graphe (pas obligatoire)
    
    Retourne :
        resultat de test de corélation linéaire
        + formule de la droite de regression
    """
    if not isinstance(var1, str) or not isinstance(var2, str):
        raise TypeError("var1 et var2 doivent être des noms de colonnes (string).")

    if var1 not in df.columns or var2 not in df.columns:
        raise ValueError(f"La colonne {var1} ou {var2} n'existe pas dans le dataframe.")
    
    if df[var1].dtype not in ["int64", "float64"]:
        raise ValueError(f"La colonne {var1} n'est pas numérique.")
    
    if df[var2].dtype not in ["int64", "float64"]:
        raise ValueError(f"La colonne {var2} n'est pas numérique.")
    
            
    # Model de regression linéaire simple
    model = LinearRegression()
    model.fit(df[[var1]], df[[var2]])

    # Creation droite de regression
    droite_pred = lambda x: model.intercept_ + x*model.coef_
    
    # Calcul du coefficient de correlation linéaire
    r, p_value = stats.pearsonr(df[var1], df[var2])

    # Affichage de r carré et de la p-value
    r2 = model.score(df[[var1]], df[[var2]])

    if p_value <= 0.05:
        res_test = False
    else:
        res_test = True

    return (droite_pred, res_test, r2*100)


if __name__ == "__main__":
    #-------------
    # Création des différents data frames
    df_jeux = pd.read_sql("SELECT * FROM jeux", bdd)
    df_a_os = pd.read_sql("SELECT * FROM a_os", bdd)
    df_a_categorie = pd.read_sql("SELECT * FROM a_categorie", bdd)
    df_a_tag = pd.read_sql("SELECT * FROM a_tag", bdd)
    df_categorie = pd.read_sql("SELECT * FROM categorie", bdd)
    df_developpeur = pd.read_sql("SELECT * FROM developpeur", bdd)
    df_os = pd.read_sql("SELECT * FROM os", bdd)
    df_editeur = pd.read_sql("SELECT * FROM editeur", bdd)
    df_genre = pd.read_sql("SELECT * FROM genre", bdd)

    # Convertir les objets pd en numériques
    list_col = ["annee", "ventes_AN","ventes_EU","ventes_JP","ventes_Autre","ventes_Global"]
    for col in list_col:
        df_jeux[col] = df_jeux[col].str.replace(",", ".")
        df_jeux[col] = pd.to_numeric(df_jeux[col], errors="coerce")

    # Premiers testes de prediction pas regression lineaire
    test1 = droite_regression(df_jeux, "prix", "ventes_Global")

    # Exemple avec un jeux à 50€
    x_donne = 50

    def infos_regression_test(droite, x):
        if not droite[1] :
            y_pred = droite[0](x)
            print("Au risque de 5%, on rejet H0. Les deux variables sont liées.")
            print(f"La droite explique {droite[2]}% des données.")
            print(y_pred)
        else :
            print("On a pas assez de preuve pour rejeté H0. Les deux variables sont indépendantes.")


    # %%
    # Vrais testes :
    # Prix et ventes_global par année
    df_2009 = df_jeux[df_jeux["annee"] == 2011]
    print(df_2009.shape)

    model_2009 = droite_regression(df_2009, "prix", "ventes_Global")
    infos_regression_test(model_2009, 25)

# %%
