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


# %%
# Fonction de scatter plot
from correlation_linéaire import scatter_plot_line

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
# Test par années seulement
# On supprime les années où il y a moins de deux observations différentes
annees = sorted(df_jeux["annee"].dropna().unique())
annees.remove("1998")
annees.remove("2000")
annees.remove("2002")
annees.remove("2005")

fig, axes = plt.subplots(5, 3, figsize=(20, 15))
axes = axes.flatten()   # transforme la grille en liste simple

for i, annee in enumerate(annees):
    df_temp = df_jeux[df_jeux["annee"] == annee]
    
    scatter_plot_line(
        df_temp,
        "prix",
        "ventes_Global",
        axes[i],
        f"Jeux sortis en {int(annee)}"
    )

plt.tight_layout()
plt.show()
# Fin test par années



# %%
#---------------
# Analyse par réstrictions et prix
# Création des 4 groupes : en fonction de l'âge de réstriction
df_jeux_age1 = df_jeux[(df_jeux["age_requis"].notna()) & (df_jeux["age_requis"]<=10)]
df_jeux_age2 = df_jeux[df_jeux["age_requis"] == 12]
df_jeux_age3 = df_jeux[df_jeux["age_requis"] == 16]
df_jeux_age4 = df_jeux[df_jeux["age_requis"] == 18]


# Afficher les quatres graphes en même temps
fig, axes = plt.subplots(2, 2, figsize=(15, 4))

scatter_plot_line(df_jeux_age1, "prix", "ventes_Global", axes[0,0], "Jeux sans restriction")
scatter_plot_line(df_jeux_age2, "prix", "ventes_Global", axes[0,1], "Jeux 12 ans")
scatter_plot_line(df_jeux_age3, "prix", "ventes_Global", axes[1,0], "Jeux 16 ans")
scatter_plot_line(df_jeux_age4, "prix", "ventes_Global", axes[1,1], "Jeux 18 ans")

plt.tight_layout()
plt.show()


# %%
#---------------
# Analyse par avis
scatter_plot_line(df_jeux, "nb_avis_pos", "nb_avis_neg", log=True)



# %%
#---------------
# Analyse par réstrictions et avis positif
# Création des 4 groupes : en fonction de l'âge de réstriction


