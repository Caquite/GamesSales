<?php
    $age_requis = $_POST['age_requis'];
    $modele = $_POST['modele'] ?? null;
    // ... etc

    echo "Modèle choisi : " . $modele;
    echo "Âge requis : " . $age_requis;
?>