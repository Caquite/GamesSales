import pandas as pd
from scipy.stats import chi2

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


    
#---------Test-----------
jeux = pd.read_csv("jeux.csv")
developpeur = pd.read_csv("developpeur.csv")
df = pd.merge(jeux,developpeur,"inner")
khi2(df,"annee","developpeur",0.05)