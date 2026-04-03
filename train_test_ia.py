# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import mysql.connector

from sklearn.inspection import permutation_importance
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split, LeaveOneOut, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
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
    df = df.dropna(subset=['ventes_Global', 'age_requis', 'prix'])
    df['genre']          = df['genre'].fillna('Unknown')
    df['id_editeur']     = df['id_editeur'].fillna(-1).astype(int)
    df['id_developpeur'] = df['id_developpeur'].fillna(-1).astype(int)
    df['nb_tags']        = df['nb_tags'].fillna(0)
    df = df.fillna(0)
    print(f"Après nettoyage NaN : {len(df)} jeux")

    seuil = df['ventes_Global'].quantile(seuil_quantile)
    df = df[df['ventes_Global'] <= seuil]
    print(f"Après suppression du top {int((1-seuil_quantile)*100)}% (seuil={seuil:.2f}M) : {len(df)} jeux")

    le_genre = LabelEncoder()
    df['genre_enc'] = le_genre.fit_transform(df['genre'])

    X     = df[VARIABLES_EXPLICATIVES]
    y     = df['ventes_Global'].values
    y_log = np.log1p(y)

    print(f"\nDataset final : {X.shape[0]} jeux, {X.shape[1]} features")
    print(f"Ventes : min={y.min():.2f}M - max={y.max():.2f}M - moyenne={y.mean():.2f}M")
    return X, y, y_log, le_genre


# ==============================================================================
# TUNING & ÉVALUATION RANDOM FOREST
# ==============================================================================

def tuner_random_forest(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    meilleur_rmse = np.inf
    meilleur_n, meilleur_depth, meilleur_split, r2_train = None, None, None, None

    for n_estimators in [100, 200, 300, 500]:
        for max_depth in [None, 5, 10, 15, 20]:
            for min_samples_split in [2, 5, 10]:

                rf = RandomForestRegressor(
                    n_estimators = n_estimators,
                    max_depth = max_depth,
                    min_samples_split = min_samples_split,
                    random_state = 42
                )
                rf.fit(X_train, y_train)
                y_pred = rf.predict(X_test)
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                r2   = r2_score(y_test, y_pred)

                if rmse < meilleur_rmse:
                    meilleur_rmse = rmse
                    r2_train = r2
                    meilleur_n = n_estimators
                    meilleur_depth = max_depth
                    meilleur_split = min_samples_split

    return meilleur_n, meilleur_depth, meilleur_split, r2_train


def evaluer_random_forest_loo(X, y, n, depth, split):
    loo = LeaveOneOut()
    liste_reelles, liste_predites = [], []

    for train_idx, test_idx in loo.split(X):
        rf = RandomForestRegressor(
            n_estimators=n, max_depth=depth,
            min_samples_split=split, random_state=42, n_jobs=-1
        )
        rf.fit(X.iloc[train_idx], y[train_idx])
        liste_predites.append(rf.predict(X.iloc[test_idx])[0])
        liste_reelles.append(y[test_idx][0])

    y_pred_loo = np.array(liste_predites)
    y_true_loo = np.array(liste_reelles)

    rmse = np.sqrt(mean_squared_error(y_true_loo, y_pred_loo))
    mae  = mean_absolute_error(y_true_loo, y_pred_loo)
    r2   = r2_score(y_true_loo, y_pred_loo)
    print(f"\nRésultats LOOCV - Random Forest")
    print(f"  RMSE : {rmse:.3f}M  |  MAE : {mae:.3f}M  |  R² : {r2:.3f}")
    return rmse, mae, r2, y_pred_loo, y_true_loo


# ==============================================================================
# TUNING & ÉVALUATION GRADIENT BOOSTING
# ==============================================================================

def tuner_gradient_boosting(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    def objective(trial):
        params = {
            'n_estimators':      trial.suggest_int('n_estimators', 50, 500, step=50),
            'learning_rate':     trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
            'max_depth':         trial.suggest_int('max_depth', 2, 8),
            'subsample':         trial.suggest_float('subsample', 0.5, 1.0),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
            'min_samples_leaf':  trial.suggest_int('min_samples_leaf', 1, 10),
            'max_features':      trial.suggest_categorical('max_features', ['sqrt', 'log2', None]),
        }

        modele = GradientBoostingRegressor(**params, random_state=42)

        scores = cross_val_score(
            modele, X_train, y_train,
            cv=5,
            scoring='neg_root_mean_squared_error',
            n_jobs=-1
        )

        return -scores.mean()  # on minimise donc on inverse

    study = optuna.create_study(
        direction='minimize',
        sampler=optuna.samplers.TPESampler(seed=42),
        pruner=optuna.pruners.MedianPruner(n_startup_trials=10)
    )
    study.optimize(objective, n_trials=100, show_progress_bar=True)

    best_params = study.best_params
    meilleur_modele = GradientBoostingRegressor(**study.best_params, random_state=42)
    meilleur_modele.fit(X_train, y_train)
    y_pred = meilleur_modele.predict(X_test)
    r2_train = r2_score(y_test, y_pred)
    #rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    #print(f"GB meilleurs hyperparamètres : {best_params}")
    #print(f"GB RMSE train/test : {rmse:.3f}M  |  R² : {r2_train:.3f}")
    return best_params, r2_train


def evaluer_gradient_boosting_loo(X, y, best_params):
    loo = LeaveOneOut()
    liste_reelles, liste_predites = [], []
    modele = GradientBoostingRegressor(**best_params, random_state=42)

    for train_idx, test_idx in loo.split(X):
        modele.fit(X.iloc[train_idx], y[train_idx])
        liste_predites.append(modele.predict(X.iloc[test_idx])[0])
        liste_reelles.append(y[test_idx][0])

    y_pred_loo = np.array(liste_predites)
    y_true_loo = np.array(liste_reelles)

    rmse = np.sqrt(mean_squared_error(y_true_loo, y_pred_loo))
    mae  = mean_absolute_error(y_true_loo, y_pred_loo)
    r2   = r2_score(y_true_loo, y_pred_loo)
    #print(f"\nRésultats LOOCV - Gradient Boosting")
    #print(f"  RMSE : {rmse:.3f}M  |  MAE : {mae:.3f}M  |  R² : {r2:.3f}")
    
    return rmse, mae, r2, y_pred_loo, y_true_loo


# ==============================================================================
# TUNING & ÉVALUATION SVR
# ==============================================================================

def tuner_svr(X, y, y_log):
    X_train, X_test, y_train_log, _ = train_test_split(X, y_log, test_size=0.2, random_state=42)
    _, _, _, y_test_reel             = train_test_split(X, y,     test_size=0.2, random_state=42)

    meilleur_rmse = np.inf
    meilleur_C, meilleur_eps, r2_train = None, None, None

    for C in [0.1, 0.5, 1, 2, 3, 4, 5, 6, 7]:
        for eps in [0.35, 0.36, 0.37, 0.38]:
            scaler         = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled  = scaler.transform(X_test)

            svr = SVR(kernel='rbf', C=C, epsilon=eps, gamma='scale')
            svr.fit(X_train_scaled, y_train_log)
            y_pred_reel = np.expm1(svr.predict(X_test_scaled))

            rmse = np.sqrt(mean_squared_error(y_test_reel, y_pred_reel))
            r2   = r2_score(y_test_reel, y_pred_reel)
            if rmse < meilleur_rmse:
                meilleur_rmse, r2_train = rmse, r2
                meilleur_C, meilleur_eps = C, eps

    print(f"SVR meilleurs hyperparamètres : C={meilleur_C}, epsilon={meilleur_eps}")
    print(f"SVR RMSE train/test : {meilleur_rmse:.3f}M")
    return meilleur_C, meilleur_eps, r2_train


def evaluer_svr_loo(X, y, y_log, C, eps):
    loo = LeaveOneOut()
    liste_reelles, liste_predites = [], []

    for train_idx, test_idx in loo.split(X):
        scaler      = StandardScaler()
        X_tr_scaled = scaler.fit_transform(X.iloc[train_idx])
        X_te_scaled = scaler.transform(X.iloc[test_idx])

        svr = SVR(kernel='rbf', C=C, epsilon=eps, gamma='scale')
        svr.fit(X_tr_scaled, y_log[train_idx])
        liste_predites.append(np.expm1(svr.predict(X_te_scaled)[0]))
        liste_reelles.append(float(y[test_idx][0]))

    y_pred_loo = np.array(liste_predites)
    y_true_loo = np.array(liste_reelles)

    rmse = np.sqrt(mean_squared_error(y_true_loo, y_pred_loo))
    mae  = mean_absolute_error(y_true_loo, y_pred_loo)
    r2   = r2_score(y_true_loo, y_pred_loo)
    print(f"\nRésultats LOOCV - SVR")
    print(f"  RMSE : {rmse:.3f}M  |  MAE : {mae:.3f}M  |  R² : {r2:.3f}")
    return rmse, mae, r2, y_pred_loo, y_true_loo


# ==============================================================================
# AFFICHAGE DES RÉSULTATS
# ==============================================================================

def afficher_resultats(rmse_rf, mae_rf, r2_rf,
                        rmse_gb, mae_gb, r2_gb,
                        rmse_svr, mae_svr, r2_svr,
                        r2_train_rf, r2_train_gb, r2_train_svr):
    df_res = pd.DataFrame({
        'Modèle':   ['Random Forest', 'Gradient Boosting', 'SVR'],
        'RMSE (M)': [rmse_rf, rmse_gb, rmse_svr],
        'MAE (M)':  [mae_rf,  mae_gb,  mae_svr],
        'R²':       [r2_rf,   r2_gb,   r2_svr],
    }).sort_values('RMSE (M)')
    print("\n--- Tableau comparatif ---")
    print(df_res.to_string(index=False))
    print(f"\nR² train vs LOOCV :")
    print(f"  RF  : train={r2_train_rf:.3f}  LOOCV={r2_rf:.3f}")
    print(f"  GB  : train={r2_train_gb:.3f}  LOOCV={r2_gb:.3f}")
    print(f"  SVR : train={r2_train_svr:.3f}  LOOCV={r2_svr:.3f}")
    return df_res


# ==============================================================================
# PIPELINE PRINCIPAL — change juste le seuil ici
# ==============================================================================

def run_pipeline(seuil_quantile):
    print(f"\n{'='*60}")
    print(f"  PIPELINE — seuil quantile : {seuil_quantile}")
    print(f"{'='*60}\n")

    # 1. Données
    df_brut = charger_donnees()
    X, y, y_log, le_genre = preprocesser(df_brut, seuil_quantile)

    # 2. Random Forest
    n, depth, split, r2_train_rf = tuner_random_forest(X, y)
    rmse_rf, mae_rf, r2_rf, y_pred_rf, y_true = evaluer_random_forest_loo(X, y, n, depth, split)

    # 3. Gradient Boosting
    best_params_gb, r2_train_gb = tuner_gradient_boosting(X, y)
    rmse_gb, mae_gb, r2_gb, y_pred_gb, _ = evaluer_gradient_boosting_loo(X, y, best_params_gb)

    # 4. SVR
    C, eps, r2_train_svr = tuner_svr(X, y, y_log)
    rmse_svr, mae_svr, r2_svr, y_pred_svr, _ = evaluer_svr_loo(X, y, y_log, C, eps)

    # 5. Résultats
    df_res = afficher_resultats(
        rmse_rf, mae_rf, r2_rf,
        rmse_gb, mae_gb, r2_gb,
        rmse_svr, mae_svr, r2_svr,
        r2_train_rf, r2_train_gb, r2_train_svr
    )

    return {
        'X': X, 'y': y, 'y_log': y_log,
        'rf':  {'n': n, 'depth': depth, 'split': split, 'y_pred': y_pred_rf},
        'gb':  {'params': best_params_gb, 'y_pred': y_pred_gb},
        'svr': {'C': C, 'eps': eps, 'y_pred': y_pred_svr},
        'y_true': y_true,
        'resultats': df_res,
    }


# ==============================================================================
# LANCEMENT — modifie uniquement les seuils ici
# ==============================================================================

# %%
res_90 = run_pipeline(seuil_quantile=0.90)

# %%
res_70 = run_pipeline(seuil_quantile=0.70)
# %%

# ==============================================================================
# Code d'export pour l'API
# ==============================================================================

import joblib

# ==============================================================================
# EXPORT DES 4 MODÈLES
# ==============================================================================

# --- Petite entreprise (seuil bas, peu de ventes) ---
df_brut = charger_donnees()
X_small, y_small, y_log_small, le_genre_small = preprocesser(df_brut, seuil_quantile=0.70)

# RF petite entreprise
n, depth, split, _ = tuner_random_forest(X_small, y_small)
rf_small = RandomForestRegressor(n_estimators=n, max_depth=depth, min_samples_split=split, random_state=42, n_jobs=-1)
rf_small.fit(X_small, y_small)
joblib.dump(rf_small, 'rf_small.pkl')

# GB petite entreprise
best_params_gb, _ = tuner_gradient_boosting(X_small, y_small)
gb_small = GradientBoostingRegressor(**best_params_gb, random_state=42)
gb_small.fit(X_small, y_small)
joblib.dump(gb_small, 'gb_small.pkl')

joblib.dump(le_genre_small, 'le_genre_small.pkl')  # 1 seul LabelEncoder par dataset


# --- Grande entreprise (seuil moyen-haut, ventes moyennes) ---
X_big, y_big, y_log_big, le_genre_big = preprocesser(df_brut, seuil_quantile=0.90)

# RF grande entreprise
n, depth, split, _ = tuner_random_forest(X_big, y_big)
rf_big = RandomForestRegressor(n_estimators=n, max_depth=depth, min_samples_split=split, random_state=42, n_jobs=-1)
rf_big.fit(X_big, y_big)
joblib.dump(rf_big, 'rf_big.pkl')

# GB grande entreprise
best_params_gb, _ = tuner_gradient_boosting(X_big, y_big)
gb_big = GradientBoostingRegressor(**best_params_gb, random_state=42)
gb_big.fit(X_big, y_big)
joblib.dump(gb_big, 'gb_big.pkl')

joblib.dump(le_genre_big, 'le_genre_big.pkl')

joblib.dump(VARIABLES_EXPLICATIVES, 'features.pkl')  # commun aux 4 modèles