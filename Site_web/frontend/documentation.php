<?php
session_start();

$donnees = [
    'gradient_boosting' => [
        'type1' => ['RMSE' => '0.833', 'MAE' => '0.669', 'R²' => '0.202', 'image' => 'images/graphe_VP_vs_VR_GB_moyen.png'],
        'type2' => ['RMSE' => '0.229', 'MAE' => '0.173', 'R²' => '0.173', 'image' => 'images/graphe_VP_vs_VR_GB_petit.png'],
        'type3' => ['RMSE' => '0.757', 'MAE' => '0.603', 'R²' => '0.246', 'image' => 'images/graphe_VP_vs_VR_GB_datacomplet.png'],

    ],
    'random_forest' => [
        'type1' => ['RMSE' => '0.846', 'MAE' => '0.679', 'R²' => '0.177', 'image' => 'images/graphe_VP_vs_VR_RF_moyen.png'],
        'type2' => ['RMSE' => '0.229', 'MAE' => '0.173', 'R²' => '0.169', 'image' => 'images/graphe_VP_vs_VR_RF_petit.png'],
        'type3' => ['RMSE' => '0.763', 'MAE' => '0.608', 'R²' => '0.232', 'image' => 'images/graphe_VP_vs_VR_RF_datacomplet.png'],

    ],
];

$explications = [
    'gradient_boosting' => "Le Gradient Boosting est un algorithme d'ensemble qui construit des arbres de décision séquentiellement. Chaque arbre corrige les erreurs du précédent, ce qui le rend très performant mais plus lent à entraîner.",
    'random_forest'     => "Le Random Forest est un algorithme d'ensemble qui construit plusieurs arbres de décision en parallèle sur des sous-échantillons aléatoires. Il est robuste au surapprentissage et rapide à entraîner.",
    ];


$description_graphe = [
    'gradient_boosting' => [
        'type1' => "Avec un RMSE de 0.833 et un R² de 0.202, Gradient Boosting est le plus performant des deux modèles. Ses points s'alignent relativement mieux autour de la ligne rouge pour les ventes faibles à moyennes (0-1,5M). Cependant, comme les autres modèles, il sous-estime systématiquement les ventes élevées (>2M), où les points s'éloignent nettement de la diagonale.",
        'type2' => "Avec un RMSE de 0,229 et un R² de 0,173, Gradient Boosting est le plus performant des deux modèles. Ses points s'alignent relativement mieux autour de la ligne rouge pour les ventes faibles à moyennes (0–0,4M). Cependant, au-delà de 0,4M, la dispersion augmente nettement et les prédictions deviennent peu fiables. Gradient Boosting est légèrement supérieur à Random Forest grâce à son R² plus élevé.",
        'type3' => "Avec un RMSE de 0.757 et un R² = 0.246, Gradient Boosting est le plus performant des trois. Ses points s'alignent relativement mieux autour de la ligne rouge pour les ventes faibles à moyennes (0-1.5M). Cependant, comme les autres modèles, il sous-estime systématiquement les ventes élevées (>2M), où les points s'éloignent nettement de la diagonale.",
    ],
    'random_forest' => [
        'type1' => "Random Forest affiche des résultats très proches (RMSE = 0,846, R² = 0,177). La distribution de ses points (en bleu) est similaire à celle du Gradient Boosting, avec une légère dispersion supplémentaire pour les ventes entre 0 et 1M. Il échoue lui aussi à prédire les valeurs au dessus de 2M.",
        'type2' => "Random Forest affiche des résultats identiques (RMSE = 0,229, R² = 0,169). La distribution de ses points est similaire à celle du Gradient Boosting, avec une dispersion comparable sur la plage 0–0,4M. Il échoue lui aussi à prédire de manière fiable les valeurs au-dessus de 0,4M.",
        'type3' => "Random Forest affiche des résultats très proches (RMSE=0.763, R²=0.232). La distribution de ses points (en bleu) est similaire à celle du Gradient Boosting, avec une légère dispersion supplémentaire pour les ventes entre 0 et 1M. Il échoue lui aussi à prédire les valeurs au dessus de 2M."

        ],

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

<body class="page-documentation">
    <header>
        <div class="top_bar">
            <div class="retour_dev">
                <p><a href="index.php"> <br> <strong> Retour aux <br> prédictions </strong> </a></p>
            </div>

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
                        </select>

                        <?php if ($modele): ?>
                        <select name="type_docu" onchange="this.form.submit()">
                            <option value="">-- Choisir le type --</option>
                            <option value="type3" <?= $type === 'type3' ? 'selected' : '' ?>>Grand jeu de données</option>
                            <option value="type1" <?= $type === 'type1' ? 'selected' : '' ?>>Moyen jeu de données</option>
                            <option value="type2" <?= $type === 'type2' ? 'selected' : '' ?>>Petit jeu de données</option>
                        </select>
                        <?php endif; ?>
                    </form>
                    <?php if (!$modele): ?>
                        <p>Les types de modèles servent à étudier les capacités de chacun des trois modèles avec un petit, moyen ou grand jeu de données.
                        Cela permet d'ajuster un maximum le modèle choisi pour prédire à partir de nos données.</p>
                    <?php endif; ?>

                    <?php if ($modele && isset($explications[$modele])): ?>
                        <p class="explication_modele"><?= $explications[$modele] ?></p>
                    <?php endif; ?>
                </div>

                <div class="bloc_tableau">
                    <h4>Comparaison des modèles</h4>
                    <table>
                        <tr>
                            <td></td>
                            <td>Gradient Boosting</td>
                            <td>Random Forest</td>
                        </tr>
                        <tr>
                            <td>RMSE</td>
                            <td><?= $donnees['gradient_boosting'][$type]['RMSE'] ?? '—' ?></td>
                            <td><?= $donnees['random_forest'][$type]['RMSE'] ?? '—' ?></td>
                        </tr>
                        <tr>
                            <td>MAE</td>
                            <td><?= $donnees['gradient_boosting'][$type]['MAE'] ?? '—' ?></td>
                            <td><?= $donnees['random_forest'][$type]['MAE'] ?? '—' ?></td>
                        </tr>
                        <tr>
                            <td>R²</td>
                            <td><?= $donnees['gradient_boosting'][$type]['R²'] ?? '—' ?></td>
                            <td><?= $donnees['random_forest'][$type]['R²'] ?? '—' ?></td>
                        </tr>
                    </table>

                </div>

            </div>

            <div class="bloc_droit">
                <?php if ($valeurs): ?>
                    <img src="<?= $valeurs['image'] ?>" alt="Graphique">
                    <?php if ($modele && $type && isset($description_graphe[$modele][$type])): ?>
                        <p class="description_graphe"><?= $description_graphe[$modele][$type] ?></p>
                    <?php endif; ?>
                <?php else: ?>
                    <p>Sélectionnez un modèle et un type pour voir le graphique.</p>
                <?php endif; ?>
            </div>
        </div>

        <div class="interpretation">
            <h3>Interprétation des métriques et conclusion</h3>

            <p>
                Le RMSE mesure <strong>l'écart moyen entre les valeurs prédites et les valeurs réelles</strong> 
                (ventes en millions), en accentuant les grandes erreurs du fait de la mise au carré. 
                Le MAE mesure également cet écart moyen, mais de manière linéaire, sans donner de poids 
                excessif aux erreurs importantes. Lorsque le RMSE est plus élevé que le MAE, cela indique 
                que le modèle commet quelques erreurs particulièrement importantes qui tirent le RMSE vers 
                le haut. L'utilisation conjointe des deux métriques informe à la fois sur la distribution 
                des erreurs et sur leur magnitude.
            </p>

            <p>
                Dans notre cas, <strong>le RMSE et le MAE sont les métriques les plus pertinentes</strong> 
                pour évaluer nos modèles. Ce qui nous intéresse concrètement c'est de savoir de combien de 
                millions d'exemplaires le modèle se trompe en moyenne — ce que mesurent directement ces deux 
                métriques. Le R² quant à lui mesure la part de variance expliquée par le modèle : un R² de 1 
                indique une explication complète des données, un R² de 0 indique une absence totale de pouvoir 
                explicatif. Bien que nos R² restent faibles (maximum 24,6%), cela ne signifie pas que nos 
                modèles sont inutiles — un modèle peut avoir un R² faible tout en produisant des prédictions 
                utiles si ses erreurs absolues restent raisonnables. C'est exactement notre situation : la 
                variabilité des ventes de jeux vidéo est très difficile à capturer complètement, notamment 
                à cause de facteurs imprévisibles comme le bouche-à-oreille ou les tendances du marché.
            </p>

            <p>
                <strong>En conclusion</strong>, Gradient Boosting <strong>domine ou égale Random Forest 
                sur toutes nos configurations</strong> et offre les meilleures prédictions. SVR n'est jamais 
                le meilleur modèle. Gradient Boosting est donc le meilleur choix parmi les trois pour prédire 
                les ventes de jeux vidéo, même si ses performances restent limitées par la nature imprévisible 
                du marché.
            </p>
        </div>

    </div>

</body>
</html>