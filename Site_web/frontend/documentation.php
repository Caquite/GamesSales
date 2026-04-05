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
                <p><a href="prediction.php"> <br> <strong> Retour aux <br> prédictions </strong> </a></p>
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
                            <option value="">-- Choisir le type de développeur --</option>
                            <option value="type3" <?= $type === 'type3' ? 'selected' : '' ?>>tous types</option>
                            <option value="type1" <?= $type === 'type1' ? 'selected' : '' ?>>Intermédiaires</option>
                            <option value="type2" <?= $type === 'type2' ? 'selected' : '' ?>>Petits</option>
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
            <h3>Pertinence du choix des modèles et de l'algorithme</h3>
            <p><strong>Gradient Boosting</strong> est un modèle de machine learning qui construit des <strong>arbres de décision séquentiellement</strong>. 
            Chaque arbre <strong>corrige les erreurs du précédent</strong>, ce qui le rend très performant mais plus lent à entraîner.
            Un des principaux avantages de ce modèle est sa <strong>précision prédictive élevée</strong>. 
            Cependant, il présente un inconvénient majeur : il est particulièrement exposé au <strong>surapprentissage</strong>, ce qui signifie que le modèle devient "trop adapté" 
            aux données d'entraînement et perd sa capacité à généraliser. Pour y remédier, nos professeurs nous ont recommandé l'utilisation d'<strong>Optuna</strong>, 
            un framework open-source d'<strong>optimisation automatique des hyperparamètres</strong>, que nous avons employé afin de déterminer les meilleures configurations pour notre modèle 
            </p>

            <p><strong>Random Forest</strong> est un modèle de machine learning qui combine <strong>plusieurs arbres de décision</strong>, 
            entraînés indépendamment sur des <strong>sous-échantillons aléatoires</strong> des données. Chaque arbre produit une prédiction, et le résultat final est obtenu en faisant 
            la <strong>moyenne de toutes ces prédictions</strong>. En diversifiant ainsi les arbres, le Random Forest capture efficacement les <strong>relations complexes</strong> entre les 
            caractéristiques tout en <strong>réduisant la variance</strong>.
            Un des principaux avantages de ce modèle est sa <strong>robustesse naturelle face au surapprentissage</strong> (contrairement à Gradient Boosting), 
            grâce à la diversité des arbres qui le composent. Cependant, il peut manquer de précision sur certains datasets complexes par rapport à des méthodes séquentielles 
            comme le Gradient Boosting. Pour optimiser ses performances, nous avons également utilisé <strong>Optuna</strong> afin de déterminer les meilleures configurations.
            Avec <strong>22 variables</strong> dont une majorité de <strong>variables binaires</strong> (os, catégories), le Random Forest est particulièrement pertinent car il sélectionne aléatoirement un 
            sous-ensemble de variables à chaque arbre, évitant ainsi que certaines <strong>variables très corrélées</strong> (comme cat_solo et cat_multi) ne dominent les prédictions. 
            De plus, avec <strong>782 observations</strong>, sa robustesse naturelle face au surapprentissage en fait un <strong>choix évident</strong> pour notre dataset de taille modérée.              
            </p>


             
            <p>Pour évaluer nos modèles, nous avons choisi la méthode de validation croisée <strong>LOOCV (Leave-One-Out Cross-Validation)</strong>. 
            Cette méthode consiste à <strong>mettre de côté un seul jeu</strong>, lors de chaque itération, afin de tester le modèle, et d'utiliser 
            <strong>tous les autres pour l'entraîner</strong>. On répète cette opération pour <strong>chacune des 782 observations</strong> de notre dataset.
            Nous avons choisi le LOOCV car notre dataset est de <strong>taille limitée</strong> (782 observations). Cette méthode permet d'utiliser un 
            <strong>maximum de données pour l'entraînement</strong> tout en évaluant le modèle sur chaque observation, ce qui donne une estimation 
            <strong>très précise et fiable des performances</strong>. Cependant, elle présente un inconvénient : elle est <strong>coûteuse en calcul</strong>, 
            car le modèle doit être entraîné autant de fois qu'il y a d'observations. Dans notre cas, avec 782 jeux, cela représente <strong>782 entraînements</strong> 
            par modèle, ce qui reste acceptable.
            </p>


            <h3>Interprétation des métriques et conclusion</h3>

            <p>Le <strong>RMSE (Root Mean Squared Error)</strong> est la <strong>racine carrée de la moyenne des erreurs au carré</strong>. 
            Elle <strong>pénalise fortement les grandes erreurs</strong> de prédiction. Plus elle est <strong>proche de 0</strong>, meilleur est le modèle.</p>

            <p>La <strong>MAE (Mean Absolute Error)</strong> est la <strong>moyenne des valeurs absolues des erreurs</strong>. Elle indique en moyenne de combien 
            d'<strong>unités de ventes</strong> le modèle se trompe. Contrairement au RMSE, elle <strong>ne pénalise pas excessivement les grandes erreurs</strong>. 
            Cela en fait une métrique plus <strong>robuste</strong> pour notre dataset qui contient des jeux aux <strong>ventes très variables</strong>. 
            Ici encore, plus la valeur est <strong>proche de 0</strong>, plus le modèle est performant.</p>

            <p>Le <strong>R² (Coefficient de Détermination)</strong> mesure la <strong>proportion de la variance des ventes</strong> expliquée par notre modèle. 
            Sa valeur est comprise entre <strong>0 et 1</strong>. Plus il est <strong>proche de 1</strong>, mieux le modèle explique les variations de ventes entre les jeux. 
            Un R² de <strong>0.8</strong> par exemple signifie que notre modèle explique <strong>80% des variations de ventes</strong> observées.</p>

            <p>Ces trois métriques sont <strong>complémentaires</strong> et permettent d'avoir une <strong>vision complète et globale</strong> des performances de nos modèles. 
            Le RMSE et le MAE mesurent toutes les deux les <strong>erreurs de prédiction en unités de ventes</strong>, mais de manière différente avec chacune leurs points forts : 
            le RMSE est plus <strong>sensible aux grandes erreurs ponctuelles</strong>, tandis que le MAE donne une vision plus <strong>globale et stable</strong> de l'erreur moyenne. 
            Le R² quant à lui apporte une <strong>perspective différente</strong> en indiquant la mesure dans laquelle notre modèle explique les <strong>variations de ventes</strong> entre les jeux.</p>
        </div>

    </div>

</body>
</html>