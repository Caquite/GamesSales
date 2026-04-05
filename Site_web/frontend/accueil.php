<?php
    session_start();
    $type_dev = $_SESSION["type_dev"] ?? null;
?>

<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="style/style.css">
    <script> const TYPE_DEV = "<?php echo $_SESSION['type_dev'] ?? 'petit'; ?>"; </script>
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="js/script.js"></script>
    <title>GamesSales</title>
</head>

<body>
    <header>
        <div class="top_bar">
            <div class="retour_dev">
                <div class="choix-actuel">
                    <?php if ($type_dev): ?>
                        <span>Profil : <?= $type_dev ?> dev</span>
                        <a href="choix_dev.php"> <br> <strong> Changer de profil ? </strong> </a>
                    <?php else: ?>
                        <a href="choix_dev.php">Sélectionner profil</a>
                    <?php endif; ?>
                </div>
            </div>

            <h2> Prédiction de ventes </h2>

            <div class="plus_info">
                <button class="info">?</button>
                <div class="info_popup" id="infoPopup">
                    <p>Bienvenue dans GamesSales, le site de prédiction de ventes. Ici, vous pouvez visualiser les prédictions de ventes pour différents jeux.
                        Il vous suffit d'entrer les données de votre jeu dans la section "Vos données", de choisir un modèle de prédiction dans la 
                        section "Choix du modèle", et les résultats seront affichés dans la section "Résultats". <br>
                        <strong style="color:#e14c4c;"> Si vous ne connaissez pas certaines données veuillez saisir "0". </strong>
                    </p>
                </div>

            </div>
        </div>
    </header>

    <div class="bloc1">
        <h4>Vos données</h4>

        <form id="formPred" method="POST">
            <div class="tables_grid">

                <!-- Colonne 1 -->
                <table class="tableau_donnees">
                    <tbody>
                        <tr><td>âge requis</td><td><select name="age_requis">
                            <option value="">-</option>
                            <option value="0">0</option>
                            <option value="7">7</option>
                            <option value="12">12</option>
                            <option value="16">16</option>
                            <option value="18">18</option>
                        </select></td></tr>
                        <tr><td>nombre de succès</td><td><input type="number" name="nb_succes" min="0" step="1"></td></tr>
                        <tr><td>temps de jeu moyen <small>(en minutes)</small></td><td><input type="number" name="temps_jeu_moyen" min="0" step="0.01"></td></tr>
                        <tr><td>prix</td><td><input type="number" name="prix" min="0" step="0.01"></td></tr>
                        <tr><td>avis positifs</td><td><input type="number" name="nb_avis_pos" min="0" step="1"></td></tr>
                        <tr><td>avis négatifs</td><td><input type="number" name="nb_avis_neg" min="0" step="1"></td></tr>
                        <tr><td>genre</td><td><select name="genre_enc">
                            <option value="">-</option>
                            <option value="Action">Action</option>
                            <option value="Shooter">Shooter</option>
                            <option value="Role-Playing">Role-Playing</option>
                            <option value="Simulation">Simulation</option>
                            <option value="Platform">Platform</option>
                            <option value="Strategy">Strategy</option>
                            <option value="Fighting">Fighting</option>
                            <option value="Adventure">Adventure</option>
                            <option value="Racing">Racing</option>
                            <option value="Misc">Misc</option>
                            <option value="Sports">Sports</option>
                            <option value="Puzzle">Puzzle</option>
                        </select></td></tr>
                        <tr><td>éditeur
                            <small class="info-inconnu" id="info_editeur" style="color:#e14c4c; display:none;">
                                (Éditeur inconnu)
                            </small></td><td>
                            <input type="text" name="id_editeur" id="input_editeur" list="liste_editeurs" placeholder="Tapez un éditeur...">
                            <datalist id="liste_editeurs"></datalist>
                        </td></tr>
     
                    </tbody>
                </table>

                <!-- Colonne 2 -->
                <table class="tableau_donnees">
                    <tbody>
                        <tr><td>développeur
                            <small class="info-inconnu" id="info_developpeur" style="color:#e14c4c; display:none;">
                                (Développeur inconnu)
                            </small></td><td>
                            <input type="text" name="id_developpeur" id="input_developpeur" list="liste_developpeurs" placeholder="Tapez un développeur...">
                            <datalist id="liste_developpeurs"></datalist>
                        </td></tr>
                        <tr><td>sur Windows ?</td><td><select name="os_windows">
                            <option value="">-</option>
                            <option value="1">Oui</option>
                            <option value="0">Non</option>
                        </select></td></tr>
                        <tr><td>sur Mac ?</td><td><select name="os_mac">
                            <option value="">-</option>
                            <option value="1">Oui</option>
                            <option value="0">Non</option>
                        </select></td></tr>
                        <tr><td>sur Linux ?</td><td><select name="os_linux">
                            <option value="">-</option>
                            <option value="1">Oui</option>
                            <option value="0">Non</option>
                        </select></td></tr>
                        <tr><td>catégorie multi-joueurs ?</td><td><select name="cat_multi">
                            <option value="">-</option>
                            <option value="1">Oui</option>
                            <option value="0">Non</option>
                        </select></td></tr>
                        <tr><td>catégorie en ligne ?</td><td><select name="cat_online">
                            <option value="">-</option>
                            <option value="1">Oui</option>
                            <option value="0">Non</option>
                        </select></td></tr>
                        <tr><td>catégorie vacances ?</td><td><select name="cat_vac">
                            <option value="">-</option>
                            <option value="1">Oui</option>
                            <option value="0">Non</option>
                        </select></td></tr>
                        <tr><td>catégorie solo ?</td><td><select name="cat_solo">
                            <option value="">-</option>
                            <option value="1">Oui</option>
                            <option value="0">Non</option>
                        </select></td></tr>
                    </tbody>
                </table>

                <!-- Colonne 3 -->
                <table class="tableau_donnees">
                    <tbody>
                        <tr><td>catégorie cloud ?</td><td><select name="cat_cloud">
                            <option value="">-</option>
                            <option value="1">Oui</option>
                            <option value="0">Non</option>
                        </select></td></tr>
                        <tr><td>catégorie achivement ?</td><td><select name="cat_achiev">
                            <option value="">-</option>
                            <option value="1">Oui</option>
                            <option value="0">Non</option>
                        </select></td></tr>
                        <tr><td>catégorie cartes ?</td><td><select name="cat_cards">
                            <option value="">-</option>
                            <option value="1">Oui</option>
                            <option value="0">Non</option>
                        </select></td></tr>
                        <tr><td>catégorie contrôles ?</td><td><select name="cat_ctrl">
                            <option value="">-</option>
                            <option value="1">Oui</option>
                            <option value="0">Non</option>
                        </select></td></tr>
                        <tr><td>catégorie workshop ?</td><td><select name="cat_workshop">
                            <option value="">-</option>
                            <option value="1">Oui</option>
                            <option value="0">Non</option>
                        </select></td></tr>
                        <tr><td>nombre de tag</td><td><input type="number" name="nb_tags"></td></tr>
                        </select></td></tr>
                        <tr><td><button type="button" id="btn_reset" class="btn_reset"> Réinitialiser </button></td></tr>
                    </tbody>
                </table>

            </div>

        </form>
    </div>

    <div class="contener">
        <div class="bloc2">
            <h3> Choix du modèle </h3>

            <select id="monMenu" name="modele" form="formPred">
                <option value="">-- Choisir le modèle --</option>
                <option value="gb">Gradient Boosting</option>
                <option value="rf">Random Forest</option>
            </select>
            <button type="submit" form="formPred" class="btn_submit">Envoyer</button>

            <p> Choisissez le modèle de prédiction à utiliser pour estimer les ventes du jeu. <br>
            Remarque : le modèle Gradient Boosting est le meilleur modèle, quel que soit votre profil. </p>
            <p class="info_modeles">Pour plus d'informations sur les modèles de prédiction, veuillez appuiller <a href="documentation.php">ici</a>.</p>

        </div>

        <div class="bloc3">
            <h3> Résultats </h3>

            <p> (Pas d'unité particulière pour le résultat) </p>

        </div>

    </div>
    
</body>
</html>