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

        $('input, select', this).each(function() {
            const val = $(this).val().trim();
            const nom = $(this).attr('name');
            if (val === '' || val === null) {
                erreurs.push('Le champ "' + nom + '" est vide.');
                $(this).css('border-color', 'red');
            } else {
                $(this).css('border-color', '#ccc');
            }
        });

        const champsNumeriques = [
            'nb_succes', 'temps_jeu_moyen', 'prix',
            'nb_avis_pos', 'nb_avis_neg', 'nb_tags'
        ];

        champsNumeriques.forEach(function(nom) {
            const input = $('input[name="' + nom + '"]');
            let val = input.val();
            val = val.replace(',', '.');
            if (val !== '' && isNaN(val)) {
                erreurs.push('Le champ "' + nom + '" doit être un nombre.');
                input.css('border-color', 'red');
            } else {
                input.val(val);
            }
        });

        if (erreurs.length > 0) {
            alert('Erreurs :\n' + erreurs.join('\n'));
            return;
        }

        // ------------------------------------------
        // ENVOIE À L'API

        const data = {
            client_type:     "<?php echo $_SESSION['type_dev'] ?? 'small'; ?>" === "grand" ? "big" : "small",
            modele:          $('#monMenu').val(),
            genre:           $('[name="genre_enc"]').val(),
            age_requis:      parseFloat($('[name="age_requis"]').val()),
            nb_succes:       parseFloat($('[name="nb_succes"]').val()),
            nb_avis_pos:     parseFloat($('[name="nb_avis_pos"]').val()),
            nb_avis_neg:     parseFloat($('[name="nb_avis_neg"]').val()),
            temps_jeu_moyen: parseFloat($('[name="temps_jeu_moyen"]').val()),
            prix:            parseFloat($('[name="prix"]').val()),
            id_editeur:      parseFloat($('[name="id_editeur"]').val()),
            id_developpeur:  parseFloat($('[name="id_developpeur"]').val()),
            os_windows:      parseFloat($('[name="os_windows"]').val()),
            os_mac:          parseFloat($('[name="os_mac"]').val()),
            os_linux:        parseFloat($('[name="os_linux"]').val()),
            cat_multi:       parseFloat($('[name="cat_multi"]').val()),
            cat_online:      parseFloat($('[name="cat_online"]').val()),
            cat_vac:         parseFloat($('[name="cat_vac"]').val()),
            cat_solo:        parseFloat($('[name="cat_solo"]').val()),
            cat_cloud:       parseFloat($('[name="cat_cloud"]').val()),
            cat_achiev:      parseFloat($('[name="cat_achiev"]').val()),
            cat_cards:       parseFloat($('[name="cat_cards"]').val()),
            cat_ctrl:        parseFloat($('[name="cat_ctrl"]').val()),
            cat_workshop:    parseFloat($('[name="cat_workshop"]').val()),
            nb_tags:         parseFloat($('[name="nb_tags"]').val()),
        };

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