<?php session_start(); ?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="style/style.css">
    <title>GamesSales</title>
</head>
<body>

    <header>
        <div class="top_bar">
            <h2>GamesSales</h2>
        </div>
    </header>

    <div class="grand_bloc_index">

        <h1> Prédisez les ventes de votre jeu vidéo ! </h1>

        <p>
            Le marché du jeu vidéo est en constante évolution et il est difficile 
            pour un développeur d'estimer à l'avance le succès commercial de son jeu. 
            GamesSales propose des outils de prédiction basés sur des modèles de Machine Learning 
            entraînés sur des données réelles de ventes de jeux vidéo.
        </p>

        <p>
            En renseignant les caractéristiques de votre jeu (genre, prix, plateformes, 
            catégories...), nos outils vous donneront des estimations des ventes mondiales 
            en millions d'exemplaires.
        </p>

        <p>
            Deux modèles sont disponibles : <strong>Random Forest</strong> et 
            <strong>Gradient Boosting</strong>. Ces modèles ont été entraînés sur 
            des données différentes selon votre profil de développeur afin de vous 
            fournir la prédiction la plus adaptée à votre situation.
        </p>

        <p> 
            <small>
            Attention : Ceci est un projet universitaire basé sur un dataset limité. 
            Les prédictions sont approximatives, ne pas trop s'y fier.
            </small>
        </p>

        <a href="choix_dev.php" class="btn_choix1"> Commencer </a>

        <footer>
            <small>
            <p>Projet réalisé dans le cadre de l'UE Science des données 4 — MIASHS Université Paul-Valéry 2025/2026</p>
            <p>Par <strong>Donia ALFONSI</strong>, <strong>Clémentine BEAULIEU</strong>, <strong>Catherine NIVAULT</strong> et <strong>Lasienica CRUZ</strong></p>
            </small>
        </footer>

    </div>

</body>
</html>