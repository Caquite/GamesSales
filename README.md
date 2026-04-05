# GamesSales — Prédiction de ventes de jeux vidéo

Projet universitaire réalisé dans le cadre de l'UE Science des données 4 (BUT Informatique 3ème année, 2025/2026).

[Accéder au site]

---

## C'est quoi ?

On a créé un site web qui permet à un développeur de jeux vidéo d'estimer les ventes mondiales de son jeu à partir de ses caractéristiques (genre, prix, plateformes, catégories...).

L'idée de départ : le marché du jeu vidéo est difficile à anticiper, surtout pour les petits studios. On a donc entraîné des modèles de Machine Learning sur des données réelles de ventes Steam pour essayer de donner une estimation.

---

## Les données

Base de données MySQL construite à partir de deux jeux de données :
 - [Accéder au site](https://www.kaggle.com/datasets/gregorut/videogamesales)
 - [Accéder au site](https://www.kaggle.com/datasets/nikdavis/steam-store-games)

On otient, grâce à ces jeux de données, des infos sur les jeux : prix, genre, nombre d'avis, temps de jeu moyen, plateformes supportées, catégories, tags, et surtout les ventes mondiales qu'on cherche à prédire.

---

## Les modèles

On a entraîné **Random Forest**, **Gradient Boosting** et **SVR** pour 3 profils différents :

- **Petit développeur** : jeux dans les 70% les moins vendus
- **Développeur intermédiaire** : jeux entre le quantile 0.50 et 0.90
- **Grand développeur** : jeux dans les 90% les moins vendus

Pour évaluer les modèles on a utilisé le **LOOCV** (Leave-One-Out Cross Validation), et pour trouver les meilleurs hyperparamètres on a utilisé un **grid search** pour Random Forest, **Optuna** (100 essais) pour Gradient Boosting et une recherche manuelle pour **SVR**.

Le Gradient Boosting ressort globalement meilleur sur toutes nos configurations.
Le SVR avait de très mauvaises performances, on l'a donc exclu du site web.

---

## Stack technique

- **Machine Learning** : Python, Scikit-learn, Optuna, Joblib
- **API** : Flask, déployée sur Render
- **Site web** : PHP, HTML, CSS, JavaScript, jQuery
- **Hébergement site** : InfinityFree

---

## Structure du projet
```
GamesSales/
├── Machine Learning/
│   ├── modeles_ml.ipynb     ← analyse complète + évaluation des modèles
│   └── export_api/          ← export des .pkl + fichiers JSON
├── Site_web/
│   ├── backend/             ← API Flask + modèles entraînés (.pkl)
│   │   ├── app.py
│   │   ├── ... .pkl
│   │   └── requirements.txt
│   └── frontend/            ← site web
│       ├── index.php
│       ├── choix_dev.php
│       ├── prediction.php
│       ├── documentation.php
│       ├── images/
│       ├── style/
│       └── js/
├── gamesales.sql           ← base de données
└── README.md
```

---

## Lancer en local
```bash
# API
cd Site_web/backend
pip install -r requirements.txt
python app.py

# Site : ouvrir avec WAMP sur localhost
```

---

## Auteurs

- **Donia ALFONSI**
- **Clémentine BEAULIEU**
- **Catherine NIVAULT**
- **Lasienica CRUZ**
