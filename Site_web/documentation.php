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
            <h2> Documentation sur les modèles utilisés </h2>

        </div>
    </header>
    
    <div class="grand_bloc">
        <h3> Explications </h3>

        <div class="bloc_soutient">
            <div class="bloc_gauche">
                <div class="bloc_modele">
                    <h4> Choisir le modèle à expliquer </h4>

                    <select id="modele_docu" name="modele_docu" form="form_model_docu">
                    <option value="">-- Choisir le modèle --</option>
                    <option value="option1">Gradient Boosting</option>
                    <option value="option2">Random Forest</option>
                    <option value="option3">SVR</option>
                </select>
                <button type="submit" form="form_model_docu" class="btn_submit">Envoyer</button>

                </div>

                <div class="bloc_tableau">
                    <h4>Comparaison des modèles</h4>
                    <table>
                        <tr>
                            <td></td>
                            <td>Grandient Boosting</td>
                            <td>Rambom Forest</td>
                            <td>SVR</td>
                        </tr>
                        <tr>
                            <td>RMSE</td>
                            <td>%</td>
                            <td>%</td>
                            <td>%</td>
                        </tr>
                        <tr>
                            <td>MAE</td>
                            <td>%</td>
                            <td>%</td>
                            <td>%</td>
                        </tr>
                        <tr>
                            <td>R²</td>
                            <td>%</td>
                            <td>%</td>
                            <td>%</td>
                        </tr>
                    </table>

                </div>

            </div>

            <div class="bloc_droit">

            </div>
        </div>

        <a href="accueil.php">Retour à la page d'accueil</a>

    </div>

</body>
</html>