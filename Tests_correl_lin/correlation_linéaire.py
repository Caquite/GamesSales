import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import importlib

if importlib.util.find_spec("sklearn") is None:
    import subprocess
    subprocess.run(["pip", "install", "scikit-learn"])

from sklearn.linear_model import LinearRegression


# Lecture du csv vgsales.csv
df = pd.read_csv("GamesSales_R/vgsales.csv")
print(df.head())

print("Dimention du df : ",df.shape)
print("Types de chaque variables du df : ",df.dtypes)

df["EU_Sales"] = df["EU_Sales"].str.replace(" €", "").str.replace(",", ".").astype(float)
df["NA_Sales"] = df["NA_Sales"].str.replace(" €", "").str.replace(",", ".").astype(float)
df["JP_Sales"] = df["JP_Sales"].str.replace(" €", "").str.replace(",", ".").astype(float)
df["Other_Sales"] = df["Other_Sales"].str.replace(" €", "").str.replace(",", ".").astype(float)
df["Global_Sales"] = df["Global_Sales"].str.replace(" €", "").str.replace(",", ".").astype(float)

print("Types de chaque variables du df : ",df.dtypes)

# Exemple de scatter plot
#plt.scatter(df["EU_Sales"], df["NA_Sales"])
#plt.xlabel("EU_Sales")
#plt.ylabel("NA_Sales")
#plt.title("Nombre de ventes d'un jeu en Europe et son équivalent en Amérique (en million?)")
#plt.show()


# ------------
# Création de la fonction pour faire un scatter plot entre deux variables quantitatives
# Version sans droite de regression
def scatter_plot(df, var1, var2):
    """
    Création d'un scatter plot pour visualiser les données.
    Arguments :
        df : data frame 
        var1 : variable pour l'axe x
        var2 : variable pour l'axe y
    
    Retourne :
        un scatter plot
    """
    if not isinstance(var1, str) or not isinstance(var2, str):
        raise TypeError("var1 et var2 doivent être des noms de colonnes (string).")

    if var1 not in df.columns or var2 not in df.columns:
        raise ValueError(f"La colonne '{var1}' ou '{var2}' n'existe pas dans le dataframe.")
    
    if df[var1].dtype not in ["int64", "float64"]:
        raise ValueError(f"La colonne '{var1}' n'est pas numérique.")
    
    if df[var2].dtype not in ["int64", "float64"]:
        raise ValueError(f"La colonne '{var2}' n'est pas numérique.")

    plt.scatter(df[var1], df[var2])
    plt.xlabel(var1)
    plt.ylabel(var2)
    plt.title(var1 + " par " + var2)
    plt.grid(linestyle='--', linewidth=0.5, alpha=0.7)
    plt.show()
    
scatter_plot(df, "EU_Sales", "NA_Sales")


# ------------
# Création de la fonction pour faire un scatter plot entre deux variables quantitatives
# Version avec droite de regression
def scatter_plot_line(df, var1, var2, titre = None):
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

    plt.scatter(df[var1], df[var2])
    plt.plot(x_range, y_pred, color="red")
    plt.xlabel(var1)
    plt.ylabel(var2)
    if titre != None:
        plt.title(var2 + " par " + var1)
    else:
        plt.title(var2 + " par " + var1)
    plt.grid(linestyle='--', linewidth=0.5, alpha=0.7)
    plt.show()

scatter_plot_line(df, "EU_Sales", "NA_Sales")

