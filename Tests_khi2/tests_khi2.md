# Test du khi2
## Importations
```python
import pandas as pd
from scipy.stats import chi2
```

## Fonction
```python
def khi2(df,colonne1,colonne2,alpha):
    """
    df: le dataframe
    colonne1 et colonne2: nom des colonnes pour le test
    sep: séparateur du csv
    alpha: degré d'erreur
    """

    #tableau de contingence
    tab_contingence = pd.crosstab(df[colonne1],df[colonne2])
    print("Tableau de contingence:\n",tab_contingence)

    eff_observes = tab_contingence.values #extrait les données du df et les met en array

    #totaux marginaux
    total = eff_observes.sum()
    totaux_lignes = eff_observes.sum(axis=1,keepdims=True)
    totaux_colonnes = eff_observes.sum(axis=0,keepdims=True)

    #Calcul des effectifs théoriques
    theorique = (totaux_lignes*totaux_colonnes)/total
    print("Effectifs théoriques:\n",pd.DataFrame(theorique,index=tab_contingence.index,columns=tab_contingence.columns))

    khi_2 = ((eff_observes-theorique)**2/theorique).sum()

    ddl= (eff_observes.shape[0]-1)*(eff_observes.shape[1]-1)

    p_value = 1 - chi2.cdf(khi_2,ddl)

    print(f"Khi² = {khi_2}")
    print(f"Degrés de liberté = {ddl}")
    print(f"p_value = {p_value}")

    #Interprétation à degré 5%
    if p_value < alpha:
        print(f'Résultat : dépendance significative entre {colonne1} et {colonne2} (p<{alpha})')
    else:
        print(f'Résultat : pas de dépendance significative entre {colonne1} et {colonne2} (p>={alpha})')
```

## Création du dataframe
```python
a_cat = pd.read_csv("gamesale_table_a_categorie.csv")
a_os = pd.read_csv("gamesale_table_a_os.csv")
a_tag = pd.read_csv("gamesale_table_a_tag.csv")
cat = pd.read_csv("gamesale_table_categorie.csv")
dev = pd.read_csv("gamesale_table_developpeur.csv")
editeur = pd.read_csv("gamesale_table_editeur.csv")
genre = pd.read_csv("gamesale_table_genre.csv")
jeux = pd.read_csv("gamesale_table_jeux.csv")
os = pd.read_csv("gamesale_table_os.csv")

df = pd.merge(jeux,dev)
df = pd.merge(df,editeur)
df = pd.merge(df,genre)
print(df.head())
```

## Développeur et catégorie
## Développeur et tag
## Développeur et OS
## Développeur et âge requis
## Développeur et année
## Catégorie et tag
## Catégorie et OS
## Catégorie et âge requis
## Catégorie et annéee
## Tag et OS
## Tag et âge requis
## Tag et année
## OS et âge requis
## OS et année
## Âge requis et année