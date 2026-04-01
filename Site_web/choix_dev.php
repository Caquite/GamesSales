<?php
session_start();
?>
<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="style/style.css">
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="js/script.js"></script>
    <title>GamesSales</title>
</head>

<body>
    <header>
        <div class="top_bar">
            <h2> Choix du developpeur </h2>

        </div>
    </header>
    
    <div class="grand_bloc">
        <p> Bienvenue dans GamesSales, le site de prédiction de ventes. Ici, vous pouvez visualiser les prédictions de ventes pour différents jeux.
            Pour commencer, veuillez séléctionner ce qui vous correspond le plus : </p>

        <div class="bloc_soutient">

            <div class="bloc_gauche_choix">
                <p> Je suis un petit développeur </p>
                <button class="btn_choix1"> <a href="accueil.php"> Choisir </a> </button>
            </div>

            <div class="bloc_gauche_choix">
                <p> Je suis un grand développeur </p>
                <button class="btn_choix2"> <a href="accueil.php"> Choisir </a> </button>
            </div>
        </div>

    </div>

</body>
</html>