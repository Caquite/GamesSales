# %%
import mysql.connector
from mysql.connector import Error

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression
import importlib

# Connexion a la base de données
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


# %%
#---------------
# Affichage des informations
print(df_jeux.columns)
print(df_jeux.dtypes)

# %%
# Convertir les objets pd en numérique
list_col = ["ventes_AN","ventes_EU","ventes_JP","ventes_Autre","ventes_Global"]
for col in list_col:
    df_jeux[col] = df_jeux[col].str.replace(",", ".")
    df_jeux[col] = pd.to_numeric(df_jeux[col], errors="coerce")
print(df_jeux.dtypes)

# %%
#---------------
# Analyse par périodes
# Création des 3 périodes : en années
df_jeux["annee"] = df_jeux["annee"].replace("", np.nan)
df_jeux_annee1 = df_jeux[(df_jeux["annee"].notna()) & (df_jeux["annee"]<"2010")]
df_jeux_annee2 = df_jeux[(df_jeux["annee"]>="2010") & (df_jeux["annee"]<"2015")]
df_jeux_annee3 = df_jeux[(df_jeux["annee"]>="2015") & (df_jeux["annee"]<"2020")]

print(df_jeux_annee3["annee"])

# %%
# Fonction de scatter plot
def scatter_plot_line(df, var1, var2, ax=None, titre=None):
    """
    Création d'un scatter plot et d'une droite de regression pour visualiser les données.
    Arguments :
        df : data frame 
        var1 : variable pour l'axe x
        var2 : variable pour l'axe y
    
    Retourne :
        un scatter plot avec une droite de regression
        + resultat de test de corélation linéaire
    """
    if not isinstance(var1, str) or not isinstance(var2, str):
        raise TypeError("var1 et var2 doivent être des noms de colonnes (string).")

    if var1 not in df.columns or var2 not in df.columns:
        raise ValueError(f"La colonne {var1} ou {var2} n'existe pas dans le dataframe.")
    
    if df[var1].dtype not in ["int64", "float64"]:
        raise ValueError(f"La colonne {var1} n'est pas numérique.")
    
    if df[var2].dtype not in ["int64", "float64"]:
        raise ValueError(f"La colonne {var2} n'est pas numérique.")
    

    # Model de regression linéaire
    model = LinearRegression()
    model.fit(df[[var1]], df[[var2]])

    # Créer les points pour tracer la droite
    x_range = np.linspace(df[var1].min(), df[var1].max(), 100)  #crée 100 points régulièrement espacés entre le min et le max de var1
    y_pred = model.predict(x_range.reshape(-1, 1))              #Sklearn attend ses données en 2D (lignes x colonnes) et x_range est en 1D, donc on reshape pour le mettre au bon format

    # Calcul du coefficient de correlation linéaire
    r, p_value = stats.pearsonr(df[var1], df[var2])

    # Affichage de r carré et de la p-value
    r2 = model.score(df[[var1]], df[[var2]])
    print(f"\nR² : {r2}")
    print(f"La droite explique {r2*100:.2f}% des données.")

    # Les hypothèses
    print("Test statistique :\n - H0 : Les deux variables sont indépendantes.\n - H1 : Les deux variables sont liées.")
    print(f"p-value : {p_value:.2e}")

    if (p_value <= 0.05):
        print(f"Au risque de 5%, on rejet H0. Les variables {var1} et {var2} sont liées.")
    else:
        print(f"On a pas assez de preuve pour rejeté H0. Les deux variables {var1} et {var2} sont indépendantes.")

    if ax != None:
        ax.scatter(df[var1], df[var2])
        ax.plot(x_range, y_pred, color="red")
        ax.set_xlabel(var1)
        ax.set_ylabel(var2)
        if titre != None:
            ax.set_title(titre)
        else:
            ax.set_title(var2 + " par " + var1)
        ax.grid(linestyle='--', linewidth=0.5, alpha=0.7)

    else:
        plt.scatter(df[var1], df[var2])
        plt.plot(x_range, y_pred, color="red")
        plt.xlabel(var1)
        plt.ylabel(var2)
        if titre != None:
            plt.title(titre)
        else:
            plt.title(var2 + " par " + var1)
        plt.grid(linestyle='--', linewidth=0.5, alpha=0.7)
        plt.show()
        

scatter_plot_line(df_jeux_annee1, "prix", "ventes_Global", titre="Vente Global par prix des jeux sortient entre 1998 et 2010")

# %%
# Afficher les trois graphes en même temps
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

scatter_plot_line(df_jeux_annee1, "prix", "ventes_Global", axes[0], "Jeux sortient entre 1998 et 2010")
scatter_plot_line(df_jeux_annee2, "prix", "ventes_Global", axes[1], "Jeux sortient entre 2010 et 2015")
scatter_plot_line(df_jeux_annee3, "prix", "ventes_Global", axes[2], "Jeux sortient entre 2015 et 2020")

plt.tight_layout()
plt.show()



# %%
#---------------
# Analyse par réstrictions
# Création des 4 groupes : en fonction de l'âge de réstriction
df_jeux_age1 = df_jeux[(df_jeux["age_requis"].notna()) & (df_jeux["age_requis"]<=10)]
df_jeux_age2 = df_jeux[df_jeux["age_requis"] == 12]
df_jeux_age3 = df_jeux[df_jeux["age_requis"] == 16]
df_jeux_age4 = df_jeux[df_jeux["age_requis"] == 18]

print(df_jeux_age1.shape)
print(df_jeux_age2.shape)
print(df_jeux_age3.shape)
print(df_jeux_age4.shape)


# Afficher les quatres graphes en même temps
fig, axes = plt.subplots(2, 2, figsize=(15, 4))

scatter_plot_line(df_jeux_age1, "prix", "ventes_Global", axes[0,0], "Jeux sortient entre 1998 et 2010")
scatter_plot_line(df_jeux_age2, "prix", "ventes_Global", axes[0,1], "Jeux sortient entre 2010 et 2015")
scatter_plot_line(df_jeux_age3, "prix", "ventes_Global", axes[1,0], "Jeux sortient entre 2015 et 2020")
scatter_plot_line(df_jeux_age4, "prix", "ventes_Global", axes[1,1], "Jeux sortient entre 2015 et 2020")

plt.tight_layout()
plt.show()


# %%
