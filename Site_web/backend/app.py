import os
import joblib
import pandas as pd
from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)     # Sans CORS, le navigateur refuse d'envoyer des requêtes vers un domaine différent pour des raisons de sécurité

modeles = {
    ('small', 'rf'): joblib.load('rf_small.pkl'),
    ('small', 'gb'): joblib.load('gb_small.pkl'),
    ('big', 'rf'): joblib.load('rf_big.pkl'),
    ('big', 'gb'): joblib.load('gb_big.pkl'),
    ('mid', 'rf'): joblib.load('rf_mid.pkl'),
    ('mid', 'gb'): joblib.load('gb_mid.pkl'),
}
encoders = {
    'small': joblib.load('le_genre_small.pkl'),
    'big':   joblib.load('le_genre_big.pkl'),
    'mid': joblib.load('le_genre_mid.pkl'),
}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # Validation des données côté serveur
    champs_obligatoires = [
        'client_type', 'modele', 'genre', 'age_requis', 'nb_succes',
        'nb_avis_pos', 'nb_avis_neg', 'temps_jeu_moyen', 'prix',
        'id_editeur', 'id_developpeur', 'os_windows', 'os_mac', 'os_linux',
        'cat_multi', 'cat_online', 'cat_vac', 'cat_solo', 'cat_cloud',
        'cat_achiev', 'cat_cards', 'cat_ctrl', 'cat_workshop', 'nb_tags'
    ]

    # Vérifier que tous les champs sont présents
    for champ in champs_obligatoires:
        if champ not in data:
            return jsonify({'erreur': f'Champ manquant : {champ}'}), 400

    # Vérifier les valeurs
    if data['client_type'] not in ['small', 'big', 'autre']:
        return jsonify({'erreur': 'client_type invalide'}), 400
    if data['modele'] not in ['rf', 'gb']:
        return jsonify({'erreur': 'modele invalide'}), 400

    # Vérifier que les champs numériques sont positifs
    champs_numeriques = [
        'age_requis', 'nb_succes', 'nb_avis_pos', 'nb_avis_neg',
        'temps_jeu_moyen', 'prix', 'os_windows', 'os_mac', 'os_linux',
        'cat_multi', 'cat_online', 'cat_vac', 'cat_solo', 'cat_cloud',
        'cat_achiev', 'cat_cards', 'cat_ctrl', 'cat_workshop', 'nb_tags'
    ]

    for champ in champs_numeriques:
        val = data[champ]
        if not isinstance(val, (int, float)):
            return jsonify({'erreur': f'{champ} doit être un nombre'}), 400
        if val < 0:
            return jsonify({'erreur': f'{champ} ne peut pas être négatif'}), 400

    # Vérifier les champs binaires
    champs_binaires = [
        'os_windows', 'os_mac', 'os_linux', 'cat_multi', 'cat_online',
        'cat_vac', 'cat_solo', 'cat_cloud', 'cat_achiev', 'cat_cards',
        'cat_ctrl', 'cat_workshop'
    ]

    for champ in champs_binaires:
        if int(data[champ]) not in [0, 1]:
            return jsonify({'erreur': f'{champ} doit être 0 ou 1'}), 400
    
    client_type = data['client_type']
    modele_type = data['modele']

    try:
        genre_enc = encoders[client_type].transform([data['genre']])[0]
    except ValueError:
        return jsonify({'erreur': f'Genre "{data["genre"]}" non reconnu'}), 400

    X = pd.DataFrame([{
        'age_requis':       data['age_requis'],
        'nb_succes':        data['nb_succes'],
        'nb_avis_pos':      data['nb_avis_pos'],
        'nb_avis_neg':      data['nb_avis_neg'],
        'temps_jeu_moyen':  data['temps_jeu_moyen'],
        'prix':             data['prix'],
        'genre_enc':        genre_enc,
        'id_editeur':       data['id_editeur'],
        'id_developpeur':   data['id_developpeur'],
        'os_windows':       data['os_windows'],
        'os_mac':           data['os_mac'],
        'os_linux':         data['os_linux'],
        'cat_multi':        data['cat_multi'],
        'cat_online':       data['cat_online'],
        'cat_vac':          data['cat_vac'],
        'cat_solo':         data['cat_solo'],
        'cat_cloud':        data['cat_cloud'],
        'cat_achiev':       data['cat_achiev'],
        'cat_cards':        data['cat_cards'],
        'cat_ctrl':         data['cat_ctrl'],
        'cat_workshop':     data['cat_workshop'],
        'nb_tags':          data['nb_tags'],
    }])

    prediction = modeles[(client_type, modele_type)].predict(X)[0]
    return jsonify({'ventes_predites_millions': round(float(prediction), 3)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)