<?php
session_start();

$donnees = [
    'gradient_boosting' => [
        'type1' => ['RMSE' => '0.757', 'MAE' => '0.603', 'R²' => '0.246', 'image' => 'images/graphe_VP_vs_VR_GB_datacomplet.png'],
        'type2' => ['RMSE' => '0.833', 'MAE' => '0.669', 'R²' => '0.202', 'image' => 'images/graphe_VP_vs_VR_GB_moyen.png'],
        'type3' => ['RMSE' => '0.229', 'MAE' => '0.173', 'R²' => '0.173', 'image' => 'images/graphe_VP_vs_VR_GB_petit.png'],
    ],
    'random_forest' => [
        'type1' => ['RMSE' => '0.762', 'MAE' => '0.608', 'R²' => '0.232', 'image' => 'images/graphe_VP_vs_VR_RF_datacomplet.png'],
        'type2' => ['RMSE' => '0.846', 'MAE' => '0.679', 'R²' => '0.177', 'image' => 'images/graphe_VP_vs_VR_RF_moyen.png'],
        'type3' => ['RMSE' => '0.229', 'MAE' => '0.173', 'R²' => '0.169', 'image' => 'images/graphe_VP_vs_VR_RF_petit.png'],
    ],
    'svr' => [
        'type1' => ['RMSE' => '0.831', 'MAE' => '0.664', 'R²' => '0.135', 'image' => 'images/graphe_VP_vs_VR_SVR_datacomplet.png'],
        'type2' => ['RMSE' => '0.879', 'MAE' => '0.707', 'R²' => '0.112', 'image' => 'images/graphe_VP_vs_VR_SVR_moyen.png'],
        'type3' => ['RMSE' => '0.324', 'MAE' => '0.300', 'R²' => '-0.663', 'image' => 'images/graphe_VP_vs_VR_SVR_petit.png'],
    ],
];

$explications = [
    'gradient_boosting' => "Le Gradient Boosting est un algorithme d'ensemble qui construit des arbres de décision séquentiellement. Chaque arbre corrige les erreurs du précédent, ce qui le rend très performant mais plus lent à entraîner.",
    'random_forest'     => "Le Random Forest est un algorithme d'ensemble qui construit plusieurs arbres de décision en parallèle sur des sous-échantillons aléatoires. Il est robuste au surapprentissage et rapide à entraîner.",
    'svr'               => "Le SVR (Support Vector Regression) cherche à trouver un hyperplan qui s'ajuste au mieux aux données dans un espace de haute dimension. Il est efficace sur les petits jeux de données mais plus lent sur les grands.",
];
$modele = $_GET['modele_docu'] ?? '';
$type   = $_GET['type_docu']   ?? '';
$valeurs = ($modele && $type) ? ($donnees[$modele][$type] ?? null) : null;

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
                    <form method="GET" action="">
                        <select name="modele_docu" onchange="this.form.submit()">
                            <option value="">-- Choisir le modèle --</option>
                            <option value="gradient_boosting" <?= $modele === 'gradient_boosting' ? 'selected' : '' ?>>Gradient Boosting</option>
                            <option value="random_forest"     <?= $modele === 'random_forest'     ? 'selected' : '' ?>>Random Forest</option>
                            <option value="svr"               <?= $modele === 'svr'               ? 'selected' : '' ?>>SVR</option>
                        </select>

                        <?php if ($modele): ?>
                        <select name="type_docu" onchange="this.form.submit()">
                            <option value="">-- Choisir le type --</option>
                            <option value="type1" <?= $type === 'type1' ? 'selected' : '' ?>>Grand</option>
                            <option value="type2" <?= $type === 'type2' ? 'selected' : '' ?>>Moyen</option>
                            <option value="type3" <?= $type === 'type3' ? 'selected' : '' ?>>Petit</option>
                        </select>
                        <?php endif; ?>
                    </form>
                    Les types de modèles servent à étuider les capactiés de chacun des trois modèles avec un petit/moyen/grand nombres de données.
                    Cela permet d'ajuster un maximum le modèle choisi pour prédire à partir de nos données.
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
                            <td><?= $donnees['gradient_boosting'][$type]['RMSE'] ?? '—' ?></td>
                            <td><?= $donnees['random_forest'][$type]['RMSE'] ?? '—' ?></td>
                            <td><?= $donnees['svr'][$type]['RMSE'] ?? '—' ?></td>
                        </tr>
                        <tr>
                            <td>MAE</td>
                            <td><?= $donnees['gradient_boosting'][$type]['MAE'] ?? '—' ?></td>
                            <td><?= $donnees['random_forest'][$type]['MAE'] ?? '—' ?></td>
                            <td><?= $donnees['svr'][$type]['MAE'] ?? '—' ?></td>
                        </tr>
                        <tr>
                            <td>R²</td>
                            <td><?= $donnees['gradient_boosting'][$type]['R²'] ?? '—' ?></td>
                            <td><?= $donnees['random_forest'][$type]['R²'] ?? '—' ?></td>
                            <td><?= $donnees['svr'][$type]['R²'] ?? '—' ?></td>
                        </tr>
                    </table>

                </div>

            </div>

            <div class="bloc_droit">
                <?php if ($valeurs): ?>
                    <img src="<?= $valeurs['image'] ?>" alt="Graphique">
                    <?php if ($modele && isset($explications[$modele])): ?>
                        <p class="explication_modele"><?= $explications[$modele] ?></p>
                    <?php endif; ?>
                <?php else: ?>
                    <p>Sélectionnez un modèle et un type pour voir le graphique.</p>
                <?php endif; ?>
            </div>
        </div>

        <a href="accueil.php">Retour à la page d'accueil</a>

    </div>

</body>
</html>