<?php
    session_start();

    // Fonction pour nettoyer les données
    function nettoyer($val) {
        return htmlspecialchars(strip_tags(trim($val)));
    }

    // Récupération sécurisée
    $age_requis      = nettoyer($_POST['age_requis']);
    $nb_succes       = nettoyer($_POST['nb_succes']);
    $temps_jeu_moyen = nettoyer($_POST['temps_jeu_moyen']);
    $prix            = nettoyer($_POST['prix']);
    $nb_avis_pos     = nettoyer($_POST['nb_avis_pos']);
    $nb_avis_neg     = nettoyer($_POST['nb_avis_neg']);
    $genre_enc       = nettoyer($_POST['genre_enc']);
    $id_editeur      = nettoyer($_POST['id_editeur']);
    $id_developpeur  = nettoyer($_POST['id_developpeur']);
    $os_windows      = nettoyer($_POST['os_windows']);
    $os_mac          = nettoyer($_POST['os_mac']);
    $os_linux        = nettoyer($_POST['os_linux']);
    $cat_multi       = nettoyer($_POST['cat_multi']);
    $cat_online      = nettoyer($_POST['cat_online']);
    $cat_vac         = nettoyer($_POST['cat_vac']);
    $cat_solo        = nettoyer($_POST['cat_solo']);
    $cat_cloud       = nettoyer($_POST['cat_cloud']);
    $cat_achiev      = nettoyer($_POST['cat_achiev']);
    $cat_cards       = nettoyer($_POST['cat_cards']);
    $cat_ctrl        = nettoyer($_POST['cat_ctrl']);
    $cat_workshop    = nettoyer($_POST['cat_workshop']);
    $nb_tags         = nettoyer($_POST['nb_tags']);
    $modele          = nettoyer($_POST['modele']);

    // Vérification côté serveur
    $erreurs = [];

    if (empty($age_requis)) $erreurs[] = "âge requis manquant";
    if (!is_numeric($nb_succes)) $erreurs[] = "nombre de succès invalide";
    if (!is_numeric($prix)) $erreurs[] = "prix invalide";
    // ... etc

    if (!empty($erreurs)) {
        die("Erreurs : " . implode(", ", $erreurs));
    }

    // Ici ton traitement (modèle de prédiction, etc.)
    echo "Données reçues et valides !";
?>