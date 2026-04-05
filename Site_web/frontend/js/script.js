$(document).ready(function() {

    // ------------------------------------------
    // PARTIE POPUP

    $('.info').on('click', function() {
        $('#infoPopup').toggleClass('visible');
    });

    $(document).on('click', function(e) {
        if (!$(e.target).closest('.plus_info').length) {
            $('#infoPopup').removeClass('visible');
        }
    });


    // ------------------------------------------
    // SAUVEGARDE À CHAQUE SAISIE
    $('#formPred input, #formPred select, #monMenu').on('change', function() {
        const nom = $(this).attr('name');
        const valeur = $(this).val();
        localStorage.setItem(nom, valeur);      // stockage navigateur (lors d'un refresh)
    });

    // ------------------------------------------
    // RESTAURATION POUR LE REFRESH
    const champs = [
        'age_requis', 'nb_succes', 'temps_jeu_moyen', 'prix',
        'nb_avis_pos', 'nb_avis_neg', 'genre_enc', 'id_editeur',
        'id_developpeur', 'os_windows', 'os_mac', 'os_linux',
        'cat_multi', 'cat_online', 'cat_vac', 'cat_solo',
        'cat_cloud', 'cat_achiev', 'cat_cards', 'cat_ctrl',
        'cat_workshop', 'nb_tags', 'modele'
    ];

    champs.forEach(function(nom) {
        const valeur = localStorage.getItem(nom);   // récupération des valeurs sauvegardées
        if (valeur !== null) {
            if (nom === 'modele') {
                $('#monMenu').val(valeur);
            } else {
                $('[name="' + nom + '"]').val(valeur);
            }
        }
    });

    // Vérification des champs binaires (0 ou 1 uniquement)
    const champsBinaires = [
        'os_windows', 'os_mac', 'os_linux', 'cat_multi', 'cat_online',
        'cat_vac', 'cat_solo', 'cat_cloud', 'cat_achiev', 'cat_cards',
        'cat_ctrl', 'cat_workshop'
    ];

    // Fonction qui force une valeur binaire entre 0 et 1
    function toBinaire(nom) {
        const val = Math.round(parseFloat($('[name="' + nom + '"]').val()));
        if (val < 0) return 0;
        if (val > 1) return 1;
        return val;
    }


    // ------------------------------------------
    // DEBUG

    const DEBUG = false;

    if (DEBUG) {
        // Afficher le modèle sélectionné
        $('#monMenu').on('change', function() {
            const valeur = $(this).val();
            console.log('Valeur choisie :', valeur);
        });

        console.log('client_type envoyé :', data.client_type);
        console.log('modele envoyé :', data.modele);
        console.log('data complet :', data);
    }


    // ------------------------------------------
    // REINITIALISATION FORMULAIRE

    // Réinitialisation du formulaire
    $('#btn_reset').on('click', function() {
        // Remet tous les champs à vide
        $('#formPred input').val('');
        $('#formPred select').val('');
        $('#monMenu').val('');
        
        // Remet les bordures en normal
        $('#formPred input, #formPred select').css('border', '');
        
        // Vide le localStorage
        champs.forEach(function(nom) {
            localStorage.removeItem(nom);
        });
        
        // Vide le bloc résultats
        $('.bloc3').html('<h3>Résultats</h3>');
    });


    // ------------------------------------------
    // PARTIE FORMULAIRE

    $('form').on('submit', function(e) {
        e.preventDefault();
        let champVide = false;
        let erreurs = [];

        // Vérifier que tous les champs sont remplis
        $('input, select', this).each(function() {
            const val = $(this).val().trim();

            // Si le champ est vide
            if (val === '' || val === null) {
                champVide = true;
                $(this).css('border', '2px solid red');
            } else {
                $(this).css('border', '');
            }
        });

        // Vérification du modèle
        if ($('#monMenu').val() === '' || $('#monMenu').val() === null) {
            champVide = true;
            $('#monMenu').css('border', '2px solid red');
        } else {
            $('#monMenu').css('border', '');
        }

        if (champVide) {
            erreurs.push('Au moins un champ est vide.');
        }

        // Champs entiers : ni virgule ni valeur négative
        const champsEntiers = [
            'nb_succes', 'temps_jeu_moyen',
            'nb_avis_pos', 'nb_avis_neg', 'nb_tags',
            'id_developpeur', 'id_editeur'
        ];

        champsEntiers.forEach(function(nom) {
            const input = $('input[name="' + nom + '"]');
            let val = parseFloat(input.val());

            if (isNaN(val)) {
                erreurs.push('Le champ "' + nom + '" doit être un nombre.');
                input.css('border', '2px solid red');
            } else if (val < 0) {
                erreurs.push('Le champ "' + nom + '" ne peut pas être négatif.');
                input.css('border', '2px solid red');
            } else {
                input.css('border', '');
            }
        });

        // Prix : virgule autorisé mais positif obligatoire
        const valPrix = parseFloat($('[name="prix"]').val());
        if (isNaN(valPrix)) {
            erreurs.push('Le champ "prix" doit être un nombre.');
            $('[name="prix"]').css('border', '2px solid red');
        } else if (valPrix < 0) {
            erreurs.push('Le champ "prix" ne peut pas être négatif.');
            $('[name="prix"]').css('border', '2px solid red');
        } else {
            $('[name="prix"]').css('border', '');
        }

        if (erreurs.length > 0) {
            alert('Au moins un des champs est vide.\nVeuillez modifier.');
            return;
        }


        // ------------------------------------------
        // ENVOIE À L'API

        const data = {
            client_type:     TYPE_DEV === "moyen" ? "big" : "small",
            modele:          $('#monMenu').val(),
            genre:           $('[name="genre_enc"]').val(),
            age_requis:      Math.round(parseFloat($('[name="age_requis"]').val())),
            nb_succes:       Math.round(parseFloat($('[name="nb_succes"]').val())),
            nb_avis_pos:     Math.round(parseFloat($('[name="nb_avis_pos"]').val())),
            nb_avis_neg:     Math.round(parseFloat($('[name="nb_avis_neg"]').val())),
            temps_jeu_moyen: Math.round(parseFloat($('[name="temps_jeu_moyen"]').val())),
            prix:            parseFloat($('[name="prix"]').val()),
            id_editeur:      Math.round(parseFloat($('[name="id_editeur"]').val())),
            id_developpeur:  Math.round(parseFloat($('[name="id_developpeur"]').val())),
            os_windows:      toBinaire('os_windows'),
            os_mac:          toBinaire('os_mac'),
            os_linux:        toBinaire('os_linux'),
            cat_multi:       toBinaire('cat_multi'),
            cat_online:      toBinaire('cat_online'),
            cat_vac:         toBinaire('cat_vac'),
            cat_solo:        toBinaire('cat_solo'),
            cat_cloud:       toBinaire('cat_cloud'),
            cat_achiev:      toBinaire('cat_achiev'),
            cat_cards:       toBinaire('cat_cards'),
            cat_ctrl:        toBinaire('cat_ctrl'),
            cat_workshop:    toBinaire('cat_workshop'),
            nb_tags:         Math.round(parseFloat($('[name="nb_tags"]').val())),
        };


        $.ajax({
            url: 'https://gamessales.onrender.com/predict',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),        // convertit objet JS en JSON pour l'API
            success: function(response) {
                $('.bloc3').html(`
                    <h3>Résultats</h3>
                    <p>Ventes prédites : <strong>${response.ventes_predites_millions} million(s)</strong></p>
                `);
            },
            error: function(xhr) {      // xhr = XMLHttpRequest : objet qui contient toutes les infos sur la requête HTTP
                console.log('Status :', xhr.status);
                console.log('Erreur :', xhr.responseText);
                $('.bloc3').html(`
                    <h3>Résultats</h3>
                    <p style="color:red;">Erreur ${xhr.status} : ${xhr.responseText}</p>
                `);
            }
        });

    });

});