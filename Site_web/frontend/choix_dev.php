<?php
    session_start();

    if (isset($_GET['reset'])) {
        unset($_SESSION["type_dev"]);
    }

    if (isset($_GET["type_dev"])) {
        $_SESSION["type_dev"] = $_GET["type_dev"];
        header("Location: prediction.php");
        exit;
    }
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
            <div class="retour_dev">
                <p><a href="index.php"> <br> <strong> Retour </strong> </a></p>
            </div>

            <h2> Choix du developpeur </h2>

        </div>
    </header>
    
    <div class="grand_bloc">
        <p> Bienvenue dans GamesSales, le site de prédiction de ventes. Ici, vous pouvez visualiser les prédictions de ventes pour différents jeux.
            Pour commencer, veuillez séléctionner ce qui vous correspond le plus : </p>

        <div class="bloc_soutient">

            <!-- PETIT DEVELOPPEUR -->
            <div class="bloc_gauche_choix">
                <p> Je suis un petit développeur </p>
                <a href="?type_dev=petit" class="btn_choix1"> Choisir </a>
            </div>

            <!-- DEVELOPPEUR MOYEN -->
            <div class="bloc_gauche_choix">
                <p> Je suis un développeur intermédiaire </p>
                <a href="?type_dev=mid" class="btn_choix3"> Choisir </a>
            </div>

            <!-- GRAND DEVELOPPEUR -->
            <div class="bloc_gauche_choix">
                <p> Toutes catégories de développeurs </p>
                <a href="?type_dev=big" class="btn_choix2"> Choisir </a>
            </div>

        </div>
    </div>

</body>
</html>