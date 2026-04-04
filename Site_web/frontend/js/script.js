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

    $('#monMenu').on('change', function() {
        const valeur = $(this).val();
        console.log('Valeur choisie :', valeur);
    });

    // ------------------------------------------
    // SAUVEGARDE À CHAQUE SAISIE
    $('#formPred input, #formPred select, #monMenu').on('change', function() {
        const nom = $(this).attr('name');
        const valeur = $(this).val();
        localStorage.setItem(nom, valeur);
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
        const valeur = localStorage.getItem(nom);
        if (valeur !== null) {
            if (nom === 'modele') {
                $('#monMenu').val(valeur);
            } else {
                $('[name="' + nom + '"]').val(valeur);
            }
        }
    });

    // ------------------------------------------
    // PARTIE FORMULAIRE

    $('form').on('submit', function(e) {
        e.preventDefault();
        let erreurs = [];

        // Vérifier que tous les champs sont remplis
        $('input, select', this).each(function() {
            const val = $(this).val().trim();
            const nom = $(this).attr('name');
            if (val === '' || val === null) {
                erreurs.push('Le champ "' + nom + '" est vide.');
                $(this).css('border', '2px solid red');
            } else {
                $(this).css('border', '');
            }
        });

        // Champs entiers (pas de virgule, pas négatif)
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

        // Prix : float autorisé mais positif obligatoire
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
            alert('Erreurs :\n' + erreurs.join('\n'));
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
            os_windows:      Math.round(parseFloat($('[name="os_windows"]').val())),
            os_mac:          Math.round(parseFloat($('[name="os_mac"]').val())),
            os_linux:        Math.round(parseFloat($('[name="os_linux"]').val())),
            cat_multi:       Math.round(parseFloat($('[name="cat_multi"]').val())),
            cat_online:      Math.round(parseFloat($('[name="cat_online"]').val())),
            cat_vac:         Math.round(parseFloat($('[name="cat_vac"]').val())),
            cat_solo:        Math.round(parseFloat($('[name="cat_solo"]').val())),
            cat_cloud:       Math.round(parseFloat($('[name="cat_cloud"]').val())),
            cat_achiev:      Math.round(parseFloat($('[name="cat_achiev"]').val())),
            cat_cards:       Math.round(parseFloat($('[name="cat_cards"]').val())),
            cat_ctrl:        Math.round(parseFloat($('[name="cat_ctrl"]').val())),
            cat_workshop:    Math.round(parseFloat($('[name="cat_workshop"]').val())),
            nb_tags:         Math.round(parseFloat($('[name="nb_tags"]').val())),
        };

        console.log('client_type envoyé :', data.client_type);
        console.log('modele envoyé :', data.modele);
        console.log('data complet :', data);

        $.ajax({
            url:         'https://gamessales.onrender.com/predict',
            method:      'POST',
            contentType: 'application/json',
            data:        JSON.stringify(data),
            success: function(response) {
                $('.bloc3').html(`
                    <h3>Résultats</h3>
                    <p>Ventes prédites : <strong>${response.ventes_predites_millions} million(s)</strong></p>
                `);
            },
            error: function(xhr) {
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