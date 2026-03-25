<?php
session_start();
?>
<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="style/style.css">
    <script src="js/script.js"></script>
    <title>GamesSales</title>
</head>

<body>
    <header>
        <div class="top_bar">
            <h2> Prédiction de ventes </h2>

            <div class="plus_info">
                <button class="info" onclick="toggleInfo()">?</button>
                <div class="info_popup" id="infoPopup">
                    <p>Bienvenue dans l'application de prédiction de ventes. Ici, vous pouvez visualiser les prédictions de ventes pour différents jeux.
                        Il vous suffit d'entrer les données de votre jeu dans la section "Vos données", de choisir un modèle de prédiction dans la 
                        section "Choix du modèle", et les résultats seront affichés dans la section "Résultats".</p>
                </div>

            </div>
        </div>
    </header>

    <div class="bloc1">
        <h4>Vos données</h4>

        <form id="formPred" action="traitement.php" method="POST">
            <div class="tables_grid">

                <!-- Colonne 1 -->
                <table class="tableau_donnees">
                    <tbody>
                        <tr><td>âge requis</td><td><input type="text" name="age_requis"></td></tr>
                        <tr><td>nombre de succès</td><td><input type="text" name="nb_succes"></td></tr>
                        <tr><td>temps de jeu moyen</td><td><input type="text" name="temps_jeu_moyen"></td></tr>
                        <tr><td>prix</td><td><input type="text" name="prix"></td></tr>
                        <tr><td>avis positifs</td><td><input type="text" name="nb_avis_pos"></td></tr>
                        <tr><td>avis négatifs</td><td><input type="text" name="nb_avis_neg"></td></tr>
                        <tr><td>genre</td><td><input type="text" name="genre_enc"></td></tr>
                        <tr><td>éditeur</td><td><input type="text" name="id_editeur"></td></tr>
                    </tbody>
                </table>

                <!-- Colonne 2 -->
                <table class="tableau_donnees">
                    <tbody>
                        <tr><td>développeur</td><td><input type="text" name="id_developpeur"></td></tr>
                        <tr><td>sur Windows ?</td><td><input type="text" name="os_windows"></td></tr>
                        <tr><td>sur Mac ?</td><td><input type="text" name="os_mac"></td></tr>
                        <tr><td>sur Linux ?</td><td><input type="text" name="os_linux"></td></tr>
                        <tr><td>multi-joueurs ?</td><td><input type="text" name="cat_multi"></td></tr>
                        <tr><td>en ligne ?</td><td><input type="text" name="cat_online"></td></tr>
                        <tr><td>vacances ?</td><td><input type="text" name="cat_vac"></td></tr>
                        <tr><td>solo ?</td><td><input type="text" name="cat_solo"></td></tr>
                    </tbody>
                </table>

                <!-- Colonne 3 -->
                <table class="tableau_donnees">
                    <tbody>
                        <tr><td>cloud ?</td><td><input type="text" name="cat_cloud"></td></tr>
                        <tr><td>accomplissements ?</td><td><input type="text" name="cat_achiev"></td></tr>
                        <tr><td>cartes ?</td><td><input type="text" name="cat_cards"></td></tr>
                        <tr><td>contrôles ?</td><td><input type="text" name="cat_ctrl"></td></tr>
                        <tr><td>atelier ?</td><td><input type="text" name="cat_workshop"></td></tr>
                        <tr><td>nombre de tags</td><td><input type="text" name="nb_tags"></td></tr>
                    </tbody>
                </table>

            </div>

            <button type="submit" class="btn_submit">Envoyer</button>
        </form>
    </div>

    <div class="contener">
        <div class="bloc2">
            <h3> Choix du modèle </h3>

            <select id="monMenu" name="modele" form="formPred">
                <option value="">-- Choisir le modèle --</option>
                <option value="option1">Option 1</option>
                <option value="option2">Option 2</option>
                <option value="option3">Option 3</option>
            </select>

            <p>Mini blabla</p>
            <p class="info_modeles">Pour plus d'informations sur les modèles de prédiction, veuillez appuiller <a href="documentation.php">ici</a>.</p>

        </div>

        <div class="bloc3">
            <h3> Résultats </h3>

        </div>

    </div>
    
</body>
</html>

