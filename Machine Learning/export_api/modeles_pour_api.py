# ==============================================================================
# Ce fichier sert uniquement à exporter les modèles pour l'API.
# Les hyperparamètres ont été trouvés par Optuna dans le notebook modeles_ml.ipynb,
# puis fixés en dur ici pour garantir la reproductibilité des modèles exportés.
# ==============================================================================

import pandas as pd
import warnings
import mysql.connector
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

import optuna
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")
optuna.logging.set_verbosity(optuna.logging.WARNING)


# ==============================================================================
# CHARGEMENT DES DONNÉES
# ==============================================================================

def charger_donnees():
    connexion = mysql.connector.connect(
        host     = 'localhost',
        user     = 'root',
        password = '',
        database = 'gamesale'
    )

    df = pd.read_sql("""
        SELECT id_jeu, nom_jeu, age_requis, nb_succes, nb_avis_pos,
               nb_avis_neg, temps_jeu_moyen, prix, ventes_Global
        FROM jeux
    """, connexion)
    df['ventes_Global'] = df['ventes_Global'].str.replace(',', '.').astype(float)

    df_genre = pd.read_sql("SELECT id_jeu, genre FROM genre GROUP BY id_jeu", connexion)
    df_edit  = pd.read_sql("SELECT id_jeu, id_editeur FROM editeur GROUP BY id_jeu", connexion)
    df_dev   = pd.read_sql("SELECT id_jeu, id_developpeur FROM developpeur GROUP BY id_jeu", connexion)

    df_os = pd.read_sql("""
        SELECT id_jeu,
            MAX(CASE WHEN id_os = 1 THEN 1 ELSE 0 END) AS os_windows,
            MAX(CASE WHEN id_os = 2 THEN 1 ELSE 0 END) AS os_mac,
            MAX(CASE WHEN id_os = 3 THEN 1 ELSE 0 END) AS os_linux
        FROM a_os GROUP BY id_jeu
    """, connexion)

    df_cat = pd.read_sql("""
        SELECT id_jeu,
            MAX(CASE WHEN id_cat = '1'  THEN 1 ELSE 0 END) AS cat_multi,
            MAX(CASE WHEN id_cat = '2'  THEN 1 ELSE 0 END) AS cat_online,
            MAX(CASE WHEN id_cat = '4'  THEN 1 ELSE 0 END) AS cat_vac,
            MAX(CASE WHEN id_cat = '5'  THEN 1 ELSE 0 END) AS cat_solo,
            MAX(CASE WHEN id_cat = '6'  THEN 1 ELSE 0 END) AS cat_cloud,
            MAX(CASE WHEN id_cat = '7'  THEN 1 ELSE 0 END) AS cat_achiev,
            MAX(CASE WHEN id_cat = '8'  THEN 1 ELSE 0 END) AS cat_cards,
            MAX(CASE WHEN id_cat = '10' THEN 1 ELSE 0 END) AS cat_ctrl,
            MAX(CASE WHEN id_cat = '22' THEN 1 ELSE 0 END) AS cat_workshop
        FROM a_categorie GROUP BY id_jeu
    """, connexion)

    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM a_tag LIMIT 1")
    curseur.fetchall()
    colonnes_tags = [d[0] for d in curseur.description][1:]
    somme_tags = ' + '.join([f'`{col}`' for col in colonnes_tags])
    df_tags = pd.read_sql(f"SELECT id_jeu, ({somme_tags}) AS nb_tags FROM a_tag", connexion)

    connexion.close()

    for df_merge in [df_genre, df_edit, df_dev, df_os, df_cat, df_tags]:
        df = df.merge(df_merge, on='id_jeu', how='left')

    print(f"Après fusion : {len(df)} jeux, {len(df.columns)} colonnes")
    return df


# ==============================================================================
# PRÉTRAITEMENT
# ==============================================================================

VARIABLES_EXPLICATIVES = [
    'age_requis', 'nb_succes', 'nb_avis_pos', 'nb_avis_neg',
    'temps_jeu_moyen', 'prix', 'genre_enc', 'id_editeur', 'id_developpeur',
    'os_windows', 'os_mac', 'os_linux', 'cat_multi', 'cat_online',
    'cat_vac', 'cat_solo', 'cat_cloud', 'cat_achiev', 'cat_cards',
    'cat_ctrl', 'cat_workshop', 'nb_tags',
]

def preprocesser(df, seuil_quantile):
    """Garde les jeux dont les ventes sont <= seuil_quantile (ex: 0.90 pour big)."""
    df = df.copy()
    df = df.dropna(subset=['ventes_Global', 'age_requis', 'prix'])
    df['genre']          = df['genre'].fillna('Unknown')
    df['id_editeur']     = df['id_editeur'].fillna(-1).astype(int)
    df['id_developpeur'] = df['id_developpeur'].fillna(-1).astype(int)
    df['nb_tags']        = df['nb_tags'].fillna(0)
    df = df.fillna(0)

    seuil = df['ventes_Global'].quantile(seuil_quantile)
    df = df[df['ventes_Global'] <= seuil]
    print(f"Après filtre ≤ {seuil_quantile} : {len(df)} jeux (seuil={seuil:.2f}M)")

    le_genre = LabelEncoder()
    df['genre_enc'] = le_genre.fit_transform(df['genre'])

    X = df[VARIABLES_EXPLICATIVES]
    y = df['ventes_Global'].values
    return X, y, le_genre


def preprocesser_entre(df, seuil_bas, seuil_haut):
    """Garde les jeux dont les ventes sont entre seuil_bas et seuil_haut (ex: 0.50 et 0.90 pour mid)."""
    df = df.copy()
    df = df.dropna(subset=['ventes_Global', 'age_requis', 'prix'])
    df['genre']          = df['genre'].fillna('Unknown')
    df['id_editeur']     = df['id_editeur'].fillna(-1).astype(int)
    df['id_developpeur'] = df['id_developpeur'].fillna(-1).astype(int)
    df['nb_tags']        = df['nb_tags'].fillna(0)
    df = df.fillna(0)

    seuil_b = df['ventes_Global'].quantile(seuil_bas)
    seuil_h = df['ventes_Global'].quantile(seuil_haut)
    df = df[(df['ventes_Global'] >= seuil_b) & (df['ventes_Global'] <= seuil_h)]
    print(f"Après filtre entre {seuil_bas} et {seuil_haut} : {len(df)} jeux")

    le_genre = LabelEncoder()
    df['genre_enc'] = le_genre.fit_transform(df['genre'])

    X = df[VARIABLES_EXPLICATIVES]
    y = df['ventes_Global'].values
    return X, y, le_genre


# ==============================================================================
# EXPORT DES MODÈLES POUR L'API
# ==============================================================================
# Pour chaque profil, on entraîne RF et GB sur TOUT le dataset correspondant
# (pas de train/test split ici — le LOOCV du notebook a déjà validé les modèles).
# Les hyperparamètres sont ceux trouvés par Optuna dans modeles_ml.ipynb.
#
# Les 2 profils sont :
#   - small : jeux qui font peu de ventes (≤ quantile 0.70)
#   - big   : jeux qui font beaucoup de ventes (≤ quantile 0.90)
#
# Pour chaque profil, on exporte :
#   - rf_[profil].pkl : modèle Random Forest entraîné
#   - gb_[profil].pkl : modèle Gradient Boosting entraîné
#   - le_genre_[profil].pkl : LabelEncoder du genre (nécessaire pour encoder le genre textuel en nombre lors des prédictions)
# ==============================================================================

df_brut = charger_donnees()


# ------------------------------------------------------------------------------
# PROFIL "BIG" — Grand développeur (dataset complet, ≤ quantile 0.90)
# Hyperparamètres trouvés par Optuna sur ce dataset dans modeles_ml.ipynb
# ------------------------------------------------------------------------------
X_big, y_big, le_genre_big = preprocesser(df_brut, seuil_quantile=0.90)

# Hyperparamètres RF — dataset complet
best_params_rf_big = {
    'n_estimators':    50,
    'max_depth':       12,
    'min_samples_split': 6,
    'min_samples_leaf':  1,
    'max_features':   'log2'
}
rf_big = RandomForestRegressor(**best_params_rf_big, random_state=42, n_jobs=-1)
rf_big.fit(X_big, y_big)
joblib.dump(rf_big, 'rf_big.pkl')
print("rf_big.pkl exporté")

# Hyperparamètres GB — dataset complet
best_params_gb_big = {
    'n_estimators':      300,
    'learning_rate':     0.021085345402470423,
    'max_depth':         2,
    'subsample':         0.844382925236584,
    'min_samples_split': 18,
    'min_samples_leaf':  4,
    'max_features':     'log2'
}
gb_big = GradientBoostingRegressor(**best_params_gb_big, random_state=42)
gb_big.fit(X_big, y_big)
joblib.dump(gb_big, 'gb_big.pkl')
print("gb_big.pkl exporté")

joblib.dump(le_genre_big, 'le_genre_big.pkl')
print("le_genre_big.pkl exporté")


# ------------------------------------------------------------------------------
# PROFIL "SMALL" — Petit développeur (petits jeux, ≤ quantile 0.70)
# Hyperparamètres trouvés par Optuna sur ce dataset dans modeles_ml.ipynb
# ------------------------------------------------------------------------------
X_small, y_small, le_genre_small = preprocesser(df_brut, seuil_quantile=0.70)

# Hyperparamètres RF — petits jeux
best_params_rf_small = {
    'n_estimators':      50,
    'max_depth':         4,
    'min_samples_split': 12,
    'min_samples_leaf':  6,
    'max_features':      None
}
rf_small = RandomForestRegressor(**best_params_rf_small, random_state=42, n_jobs=-1)
rf_small.fit(X_small, y_small)
joblib.dump(rf_small, 'rf_small.pkl')
print("rf_small.pkl exporté")

# Hyperparamètres GB — petits jeux
best_params_gb_small = {
    'n_estimators':      400,
    'learning_rate':     0.014385435978518381,
    'max_depth':         3,
    'subsample':         0.6235482668206153,
    'min_samples_split': 2,
    'min_samples_leaf':  10,
    'max_features':     'log2'
}
gb_small = GradientBoostingRegressor(**best_params_gb_small, random_state=42)
gb_small.fit(X_small, y_small)
joblib.dump(gb_small, 'gb_small.pkl')
print("gb_small.pkl exporté")

joblib.dump(le_genre_small, 'le_genre_small.pkl')
print("le_genre_small.pkl exporté")


print("\nTous les modèles ont été exportés avec succès !")