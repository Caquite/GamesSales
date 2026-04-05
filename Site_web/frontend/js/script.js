$(document).ready(function () {

    // ------------------------------------------
    // PARTIE POPUP

    $('.info').on('click', function () {
        $('#infoPopup').toggleClass('visible');
    });

    $(document).on('click', function (e) {
        if (!$(e.target).closest('.plus_info').length) {
            $('#infoPopup').removeClass('visible');
        }
    });


    // ------------------------------------------
    // SAUVEGARDE À CHAQUE SAISIE
    $('#formPred input, #formPred select, #monMenu').on('change', function () {
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

    champs.forEach(function (nom) {
        const valeur = localStorage.getItem(nom);   // récupération des valeurs sauvegardées
        if (valeur !== null) {
            if (nom === 'modele') {
                $('#monMenu').val(valeur);
            } else {
                $('[name="' + nom + '"]').val(valeur);
            }
        }
    });

    // ------------------------------------------
    // AUTOCOMPLETE

    function setupAutocomplete(searchId, listId, hiddenId, endpoint, labelKey, valueKey) {
        let timer = null;

        $('#' + searchId).on('input', function () {
            const q = $(this).val();
            $('#' + hiddenId).val('');
            clearTimeout(timer);

            if (q.length < 2) {
                $('#' + listId).hide().empty();
                return;
            }

            timer = setTimeout(function () {
                $.getJSON(endpoint + '&q=' + encodeURIComponent(q),
                    function (data) {
                        const list = $('#' + listId).empty();
                        if (data.length === 0) {
                            list.append('<li class="no-result">Aucun résultat</li>').show();
                            return;
                        }
                        data.forEach(function (item) {
                            $('<li>')
                                .html(`${item[labelKey]} <span class="badge-id">#${item[valueKey]}</span>`)
                                .on('click', function () {
                                    $('#' + searchId).val(item[labelKey]);
                                    $('#' + hiddenId).val(item[valueKey]);
                                    list.hide().empty();
                                })
                                .appendTo(list);
                        });
                        list.show();
                    });
            }, 300);
        });

        $(document).on('click', function (e) {
            if (!$(e.target).closest('#' + searchId).length) {
                $('#' + listId).hide();
            }
        });
    }

    setupAutocomplete('search_editeur', 'list_editeur', 'id_editeur',
        'search.php?type=editeur', 'editeur', 'id_editeur');

    setupAutocomplete('search_developpeur', 'list_developpeur', 'id_developpeur',
        'search.php?type=developpeur', 'developpeur', 'id_developpeur');




    // ------------------------------------------
    // DEBUG

    const DEBUG = false;

    if (DEBUG) {
        // Afficher le modèle sélectionné
        $('#monMenu').on('change', function () {
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
    $('#btn_reset').on('click', function () {
        // Remet tous les champs à vide
        $('#formPred input').val('');
        $('#formPred select').val('');
        $('#monMenu').val('');

        // Remet les bordures en normal
        $('#formPred input, #formPred select').css('border', '');

        // Vide le localStorage
        champs.forEach(function (nom) {
            localStorage.removeItem(nom);
        });

        // Vide le bloc résultats
        $('.bloc3').html('<h3>Résultats</h3>');
    });


    // ------------------------------------------
    // PARTIE FORMULAIRE

    $('form').on('submit', function (e) {
        e.preventDefault();
        let champVide = false;
        let erreurs = [];

        // Vérifier que tous les champs sont remplis
        $('input:not([type="hidden"]), select', this).each(function () {
            const val = $(this).val().trim();

            // Si le champ est vide
            if (val === '' || val === null) {
                champVide = true;
                $(this).css('border', '2px solid red');
            } else {
                $(this).css('border', '');
            }
        });

        if (champVide) {
            erreurs.push('Au moins un champ est vide.');
        }

        // Champs entiers : ni virgule ni valeur négative
        const champsEntiers = [
            'nb_succes', 'temps_jeu_moyen',
            'nb_avis_pos', 'nb_avis_neg', 'nb_tags'
        ];

        champsEntiers.forEach(function (nom) {
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

        if (!$('#id_editeur').val()) $('#id_editeur').val(-1);
        if (!$('#id_developpeur').val()) $('#id_developpeur').val(-1);

        const data = {
            client_type: TYPE_DEV === "moyen" ? "big" : "small",
            modele: $('#monMenu').val(),
            genre: $('[name="genre_enc"]').val(),
            age_requis: Math.round(parseFloat($('[name="age_requis"]').val())),
            nb_succes: Math.round(parseFloat($('[name="nb_succes"]').val())),
            nb_avis_pos: Math.round(parseFloat($('[name="nb_avis_pos"]').val())),
            nb_avis_neg: Math.round(parseFloat($('[name="nb_avis_neg"]').val())),
            temps_jeu_moyen: Math.round(parseFloat($('[name="temps_jeu_moyen"]').val())),
            prix: parseFloat($('[name="prix"]').val()),
            id_editeur: Math.round(parseFloat($('[name="id_editeur"]').val())),
            id_developpeur: Math.round(parseFloat($('[name="id_developpeur"]').val())),
            os_windows: Math.round(parseFloat($('[name="os_windows"]').val())),
            os_mac: Math.round(parseFloat($('[name="os_mac"]').val())),
            os_linux: Math.round(parseFloat($('[name="os_linux"]').val())),
            cat_multi: Math.round(parseFloat($('[name="cat_multi"]').val())),
            cat_online: Math.round(parseFloat($('[name="cat_online"]').val())),
            cat_vac: Math.round(parseFloat($('[name="cat_vac"]').val())),
            cat_solo: Math.round(parseFloat($('[name="cat_solo"]').val())),
            cat_cloud: Math.round(parseFloat($('[name="cat_cloud"]').val())),
            cat_achiev: Math.round(parseFloat($('[name="cat_achiev"]').val())),
            cat_cards: Math.round(parseFloat($('[name="cat_cards"]').val())),
            cat_ctrl: Math.round(parseFloat($('[name="cat_ctrl"]').val())),
            cat_workshop: Math.round(parseFloat($('[name="cat_workshop"]').val())),
            nb_tags: Math.round(parseFloat($('[name="nb_tags"]').val())),
        };


        $.ajax({
            url: 'https://gamessales.onrender.com/predict',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),        // convertit objet JS en JSON pour l'API
            success: function (response) {
                $('.bloc3').html(`
                    <h3>Résultats</h3>
                    <p>Ventes prédites : <strong>${response.ventes_predites_millions} million(s)</strong></p>
                `);
            },
            error: function (xhr) {      // xhr = XMLHttpRequest : objet qui contient toutes les infos sur la requête HTTP
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