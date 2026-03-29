$(document).ready(function() {

    // Toggle popup
    $('.info').on('click', function() {
        $('#infoPopup').toggleClass('visible');
    });

    // Ferme le popup si on clique ailleurs
    $(document).on('click', function(e) {
        if (!$(e.target).closest('.plus_info').length) {
            $('#infoPopup').removeClass('visible');
        }
    });

    // Menu déroulant
    $('#monMenu').on('change', function() {
        const valeur = $(this).val();
        console.log('Valeur choisie :', valeur);
    });

    // Validation et envoi du formulaire
    $('form').on('submit', function(e) {
        e.preventDefault();
        let erreurs = [];

        // Vérifier que tous les champs sont remplis
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

        // Vérifier que les champs numériques n'ont pas de points (remplacer par virgule)
        const champsNumeriques = [
            'nb_succes', 'temps_jeu_moyen', 'prix',
            'nb_avis_pos', 'nb_avis_neg', 'nb_tags'
        ];

        champsNumeriques.forEach(function(nom) {
            const input = $('input[name="' + nom + '"]');
            let val = input.val();
            val = val.replace(',', '.');

            // Vérifie que c'est bien un nombre
            if (val !== '' && isNaN(val)) {
                erreurs.push('Le champ "' + nom + '" doit être un nombre.');
                input.css('border-color', 'red');
            } else {
                input.val(val); // remet la valeur corrigée
            }
        });

        // Si erreurs, affiche et bloque
        if (erreurs.length > 0) {
            alert('Erreurs :\n' + erreurs.join('\n'));
            return;
        }

        // Si tout est bon, envoie
        this.submit();
    });

});