import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import LeaveOneOut
import numpy as np
import mysql.connector

connexion = mysql.connector.connect(
    host     = 'localhost',  # adresse du serveur (WAMP = localhost)
    user     = 'root',       # utilisateur par défaut sur WAMP
    password = '',           # mot de passe (vide par défaut sur WAMP)
    database = 'gamesale'    # nom de ta base de données
)


#1 table jeux
df = pd.read_sql("""
    SELECT
        id_jeu,
        nom_jeu,
        annee,
        age_requis,
        nb_succes,
        nb_avis_pos,
        nb_avis_neg,
        temps_jeu_moyen,
        prix,
        ventes_Global
    FROM jeux
""", connexion)
df['ventes_Global'] = df['ventes_Global'].str.replace(',', '.').astype(float)

print(df)

#2 table genre 
# GROUP BY id_jeu = on garde une seule ligne par jeu (le 1er genre)
df_genre = pd.read_sql("""
    SELECT id_jeu, genre
    FROM genre
    GROUP BY id_jeu
""", connexion)

print(df_genre)

#3 Table editeur
# GROUP BY id_jeu = on garde un seul éditeur par jeu (le 1er)
df_edit = pd.read_sql("""
    SELECT id_jeu, editeur
    FROM editeur
    GROUP BY id_jeu
""", connexion)

print(df_edit)

#4 table developpeur
# GROUP BY id_jeu = on garde un seul développeur par jeu (le 1er)
df_dev = pd.read_sql("""
    SELECT id_jeu, developpeur
    FROM developpeur
    GROUP BY id_jeu
""", connexion)

print(df_dev)


#5 table a_os
# id_os : 1 = Windows, 2 = Mac, 3 = Linux
# CASE WHEN id_os = 1 THEN 1 ELSE 0 END
#   -> met 1 si c'est Windows, 0 sinon
# MAX() permet de garder le 1 s'il existe parmi toutes les lignes du jeu
# GROUP BY id_jeu = une seule ligne par jeu avec les 3 colonnes OS

df_os = pd.read_sql("""
    SELECT
        id_jeu,
        MAX(CASE WHEN id_os = 1 THEN 1 ELSE 0 END) AS os_windows,
        MAX(CASE WHEN id_os = 2 THEN 1 ELSE 0 END) AS os_mac,
        MAX(CASE WHEN id_os = 3 THEN 1 ELSE 0 END) AS os_linux
    FROM a_os
    GROUP BY id_jeu
""", connexion)

print(df_os)

#6 table a_categorie
# Même logique que les OS :
# Pour chaque catégorie importante, on crée une colonne 0/1
# 1 = le jeu a cette catégorie, 0 = il ne l'a pas

df_cat = pd.read_sql("""
    SELECT
        id_jeu,
        MAX(CASE WHEN id_cat = '1'  THEN 1 ELSE 0 END) AS cat_multi,
        MAX(CASE WHEN id_cat = '2'  THEN 1 ELSE 0 END) AS cat_online,
        MAX(CASE WHEN id_cat = '4'  THEN 1 ELSE 0 END) AS cat_vac,
        MAX(CASE WHEN id_cat = '5'  THEN 1 ELSE 0 END) AS cat_solo,
        MAX(CASE WHEN id_cat = '6'  THEN 1 ELSE 0 END) AS cat_cloud,
        MAX(CASE WHEN id_cat = '7'  THEN 1 ELSE 0 END) AS cat_achiev,
        MAX(CASE WHEN id_cat = '8'  THEN 1 ELSE 0 END) AS cat_cards,
        MAX(CASE WHEN id_cat = '10' THEN 1 ELSE 0 END) AS cat_ctrl,
        MAX(CASE WHEN id_cat = '22' THEN 1 ELSE 0 END) AS cat_workshop
    FROM a_categorie
    GROUP BY id_jeu
""", connexion)

print(df_cat)


#7 table a_tag
# La table a_tag a une colonne par tag (ex: action, rpg, shooter...)
# Chaque colonne vaut 1 si le jeu a ce tag, 0 sinon
# On veut compter combien de tags chaque jeu possède au total

# Étape 1 : on récupère les noms de toutes les colonnes de la table
curseur       = connexion.cursor()
curseur.execute("SELECT * FROM a_tag LIMIT 1")
curseur.fetchall()  # nécessaire pour que .description soit disponible
toutes_cols   = [description[0] for description in curseur.description]
colonnes_tags = toutes_cols[1:]  # on enlève "id_jeu" qui est en position 0

# Étape 2 : on construit la partie SQL qui additionne tous les tags
# Résultat : "action + rpg + shooter + ..."
somme_tags = ' + '.join([f'`{col}`' for col in colonnes_tags])

# Étape 3 : on exécute la requête
df_tags = pd.read_sql(f"""
    SELECT
        id_jeu,
        ({somme_tags}) AS nb_tags
    FROM a_tag
""", connexion)

print(df_tags)


# merge() fusionne deux tableaux sur une colonne commune (ici id_jeu)
# how='left' = on garde tous les jeux de df même si une info manque

df = df.merge(df_genre, on='id_jeu', how='left')
df = df.merge(df_edit,  on='id_jeu', how='left')
df = df.merge(df_dev,   on='id_jeu', how='left')
df = df.merge(df_os,    on='id_jeu', how='left')
df = df.merge(df_cat,   on='id_jeu', how='left')
df = df.merge(df_tags,  on='id_jeu', how='left')

print(f"Fusion terminée : {len(df)} jeux | {len(df.columns)} colonnes")

# On ferme la connexion à la base de données
connexion.close()
print(df)

# 2. Variables explicatives (X) = toutes tes colonnes SAUF la cible
X = df.drop(columns=["ventes_Global","nom_jeu","id_jeu"])  # toutes les colonnes sauf "ventes"

# 3. Cible = nombre de ventes
y = df["ventes_Global"]


print("NaN par colonne :")
print(X.isna().sum())

print("Y a‑t‑il des NaN dans X ?", X.isna().any().any())

print("Taille initiale :", len(X))

# Supprimer les lignes avec NaN dans X (donc où annee est NaN)
X = X.dropna(axis=0)
y = y.loc[X.index]   # adapter y à la nouvelle taille

print("Taille après suppression :", len(X))



#enlever valeurs aberrantes avec la méthode IQR (interquartile range)

# Détecter et supprimer les outliers avec IQR (sur y = ventes)
Q1 = y.quantile(0.25)
Q3 = y.quantile(0.9)
IQR = Q3 - Q1

# Seuils pour détecter les outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"Outliers détectés : ventes < {lower_bound:.2f} ou > {upper_bound:.2f}")
print(f"Nombre d'outliers : {(y > upper_bound).sum()}")

# Supprimer les outliers supérieur à Q3
mask_outliers = (y <= upper_bound)
X = X[mask_outliers]
y = y[mask_outliers]


for col in ['editeur', 'developpeur']:
    # On compte le nombre de jeux par nom
    counts = X[col].value_counts()
    # On remplace par 'Autre' ceux qui apparaissent moins de 5 fois
    X[col] = X[col].apply(lambda x: x if counts[x] >= 5 else 'Autre')

print(f"Taille après suppression outliers : {len(X)}")

print(df['nb_tags'].describe())

#----------------

# 4. Si tu as des variables catégorielles (genre, console, etc.)
X = pd.get_dummies(X, drop_first=True) #à quoi ça sert ?

#LEAVE ONE AND OUT
# 4. Variables catégorielles → OK
X = pd.get_dummies(X, drop_first=True)
print(f"X final : {X.shape}")

y_log = np.log1p(y)

# On vérifie que X et y_log ont la même taille après les nettoyages précédents
print(f"Forme de X : {X.shape}, Forme de y_log : {y_log.shape}")

# ================================
# 1. D'ABORD : Train/Test + tuning
# ================================
X_train, X_test, y_train_log, y_test_log = train_test_split(
    X, y_log, test_size=0.2, random_state=42
)

# Tuning des hyperparamètres
best_r2 = -1
for C in [7,8,9,10,11,12,13,14,15,16]:
    for eps in [0.3,0.35,0.4,0.45,0.5,0.55,0.6]:
        svr = SVR(kernel='rbf', C=C, epsilon=eps, gamma='scale')
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        svr.fit(X_train_scaled, y_train_log)
        r2 = svr.score(X_test_scaled, y_test_log)
        if r2 > best_r2:
            best_r2 = r2
            best_C, best_eps = C, eps

print(f"Tuning → Meilleur R²: {best_r2:.3f} avec C={best_C}, ε={best_eps}")

# Modèle final train/test
scaler_final = StandardScaler()
X_train_scaled = scaler_final.fit_transform(X_train)
X_test_scaled = scaler_final.transform(X_test)
svr_final = SVR(kernel='rbf', C=best_C, epsilon=best_eps, gamma='scale')
svr_final.fit(X_train_scaled, y_train_log)
y_pred_log = svr_final.predict(X_test_scaled)

y_pred_real = np.expm1(y_pred_log)
y_test_real = np.expm1(y_test_log)
rmse_traintest = np.sqrt(mean_squared_error(y_test_real, y_pred_real))
r2_traintest = r2_score(y_test_real,y_pred_real) #R² sur une échelle réelle
print(f"Train/Test - RMSE: {rmse_traintest:.3f}, R²: {r2_traintest:.3f}")

# ================================
# 2. ENSUITE : LOOCV sur X complet
# ================================
print("\nDébut LOOCV avec cible log...")
loo = LeaveOneOut()
liste_reelles, liste_predites = [], []

for train_idx, test_idx in loo.split(X):
    X_tr = X.iloc[train_idx]
    X_te = X.iloc[test_idx]
    y_tr_log = y_log.iloc[train_idx]
    y_te_real = y.iloc[test_idx]
    
    scaler = StandardScaler()
    X_tr_scaled = scaler.fit_transform(X_tr)
    X_te_scaled = scaler.transform(X_te)
    
    svr = SVR(kernel='rbf', C=best_C, epsilon=best_eps, gamma='scale')
    svr.fit(X_tr_scaled, y_tr_log)

    pred_log = svr.predict(X_te_scaled)[0]
    pred_real = np.expm1(pred_log)
    
    liste_predites.append(pred_real)
    liste_reelles.append(float(y_te_real.iloc[0]))

y_real_all = np.array(liste_reelles)
y_pred_all = np.array(liste_predites)

rmse_loocv = np.sqrt(mean_squared_error(y_real_all, y_pred_all))
r2_loocv = r2_score(y_real_all, y_pred_all)
print(f"LOOCV - RMSE: {rmse_loocv:.3f}, R²: {r2_loocv:.3f}")

# ================================
# 3. Graphiques comparatifs
# ================================
import matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Train/Test
ax1.scatter(y_test_real, y_pred_real, alpha=0.6, color='blue')
ax1.plot([y_test_real.min(), y_test_real.max()], [y_test_real.min(), y_test_real.max()], 'r--')
ax1.set_title(f"Train/Test\nR²={best_r2:.3f}\nRMSE={rmse_traintest:.2f}")
ax1.grid(True)

# LOOCV
ax2.scatter(y_real_all, y_pred_all, alpha=0.6, color='green')
ax2.plot([y_real_all.min(), y_real_all.max()], [y_real_all.min(), y_real_all.max()], 'r--')
ax2.set_title(f"LOOCV\nR²={r2_loocv:.3f}\nRMSE={rmse_loocv:.2f}")
ax2.grid(True)

plt.tight_layout()
plt.show()




print("Ventes (y) :")
print(f"  Moyenne : {y.mean():.2f}M")
print(f"  Écart-type : {y.std():.2f}M") 
print(f"  Min : {y.min():.2f}M, Max : {y.max():.2f}M")
print(f"  RMSE relatif : {rmse_loocv/y.mean()*100:.1f}%")

print("\nX (features) :")
print(f"  {X.shape[1]} variables après get_dummies")
print(f"  Variables numériques : {X.select_dtypes(include=[np.number]).shape[1]}")


plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.hist(y, bins=30, edgecolor='black')
plt.title("Distribution des ventes")
plt.xlabel("Ventes (millions)")

plt.subplot(1,2,2)
plt.scatter(range(len(y)), np.sort(y))
plt.title("Ventes triées")
plt.ylabel("Ventes (millions)")
plt.show()


# Feature importance simple (permutation)
from sklearn.inspection import permutation_importance
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
svr = SVR(kernel='rbf', C=9, epsilon=0.3)
svr = SVR(kernel='rbf', C=best_C, epsilon=best_eps)
svr.fit(X_scaled, y_log)
result = permutation_importance(svr, X_scaled, y_log, n_repeats=10, random_state=42)
top10 = np.argsort(result.importances_mean)[-10:]
print("Top 10 variables importantes :")
for i in top10:
    print(f"  {X.columns[i]} : {result.importances_mean[i]:.4f}")



# Après ton LOOCV
residuals = y_real_all - y_pred_all
plt.figure(figsize=(12,4))

plt.subplot(1,3,1)
plt.scatter(y_pred_all, residuals, alpha=0.6)
plt.axhline(0, color='red')
plt.title("Résidus vs Prédictions")
plt.ylabel("Résidus")

plt.subplot(1,3,2)
plt.hist(residuals, bins=30, edgecolor='black')
plt.title("Distribution résidus")

plt.subplot(1,3,3)
plt.scatter(y_real_all, residuals, alpha=0.6)
plt.axhline(0, color='red')
plt.title("Résidus vs Ventes réelles")
plt.show()

