from flask import Flask, render_template
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from coinbase.wallet.client import Client
import time

app = Flask(__name__)

# Initialiser le client Coinbase avec vos informations d'identification
client = Client("API_KEY", "API_SECRET")

# Fonction pour récupérer les données historiques des prix de différentes crypto-monnaies
def get_historical_prices(crypto_symbols, period='1d'):
    historical_prices = {}
    for crypto_symbol in crypto_symbols:
        prices = client.get_spot_price(currency_pair=f'{crypto_symbol}-USD')
        historical_prices[crypto_symbol] = float(prices['amount'])
    return historical_prices

# Fonction pour normaliser les données entre 0 et 1
def normalize_data(data):
    min_price = min(data.values())
    max_price = max(data.values())
    normalized_data = {crypto_symbol: (price - min_price) / (max_price - min_price) for crypto_symbol, price in data.items()}
    return normalized_data

# Paramètres d'apprentissage
seq_length = 30  # Longueur de la séquence temporelle

# Liste des crypto-monnaies à surveiller
crypto_symbols = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH', 'ADA', 'DOT', 'XLM', 'LINK', 'USDT-USD']

# Route pour le panneau de contrôle
@app.route('/')
def control_panel():
    historical_prices = get_historical_prices(crypto_symbols)
    normalized_data = normalize_data(historical_prices)
    sequences = create_sequences(normalized_data, seq_length)
    models = build_and_train_model(sequences)  # Créer les modèles LSTM
    predictions = predict_real_time_prices(models, crypto_symbols)
    if not predictions:
        return render_template('no_predictions.html')  # Handle the case where predictions are empty
    best_crypto = select_best_crypto(predictions)
    execute_transactions(best_crypto)
    return render_template('control_panel.html', best_crypto=best_crypto, crypto_symbols=crypto_symbols, predictions=predictions)

# Fonction pour créer des séquences temporelles à partir des données historiques
def create_sequences(data, seq_length):
    sequences = {}
    for crypto_symbol in data:
        if isinstance(data[crypto_symbol], (list, np.ndarray)):  # Vérifier si c'est une liste ou un tableau numpy
            sequences[crypto_symbol] = []
            for i in range(len(data[crypto_symbol]) - seq_length):
                sequences[crypto_symbol].append(data[crypto_symbol][i:i+seq_length])
            sequences[crypto_symbol] = np.array(sequences[crypto_symbol])
        else:
            print(f"Données incorrectes pour {crypto_symbol}.")
    return sequences

# Fonction pour construire et entraîner le modèle
def build_and_train_model(sequences):
    models = {}
    for crypto_symbol in sequences:
        if isinstance(sequences[crypto_symbol], (list, np.ndarray)):  # Vérifier si c'est une liste ou un tableau numpy
            model = tf.keras.Sequential([
                layers.LSTM(50, input_shape=(sequences[crypto_symbol].shape[1], 1)),
                layers.Dense(1)
            ])
            model.compile(loss='mse', optimizer='adam')
            model.fit(sequences[crypto_symbol], np.zeros(len(sequences[crypto_symbol])), epochs=10, batch_size=32)  # Pas besoin de cibles pour l'instant
            models[crypto_symbol] = model
        else:
            print(f"Les données de séquence pour {crypto_symbol} ne sont pas valides.")
    return models

# Fonction pour prédire les mouvements de prix en temps réel
def predict_real_time_prices(models, crypto_symbols):
    real_time_prices = {}
    for crypto_symbol in crypto_symbols:
        real_time_prices[crypto_symbol] = get_crypto_price(crypto_symbol)
    normalized_real_time_prices = normalize_data(real_time_prices)
    predictions = {}
    for crypto_symbol in crypto_symbols:
        model_key = f"{crypto_symbol}-USD"  # Ajoutez le suffixe '-USD' pour correspondre aux clés dans models
        if model_key in models:
            prediction = models[model_key].predict(np.array([normalized_real_time_prices[crypto_symbol]]))[0][0]
            predictions[crypto_symbol] = prediction
        else:
            print(f"Le modèle pour {crypto_symbol} n'a pas été trouvé.")
    return predictions


# Fonction pour sélectionner la crypto-monnaie la plus adéquate
def select_best_crypto(predictions):
    best_crypto = max(predictions, key=predictions.get)
    return best_crypto

# Fonction pour effectuer des transactions
def execute_transactions(best_crypto):
    # Insérer ici la logique d'achat et de vente en fonction de la crypto-monnaie sélectionnée
    pass

# Fonction pour récupérer le prix actuel d'une crypto-monnaie à partir de Coinbase
def get_crypto_price(crypto_symbol):
    crypto_price = client.get_spot_price(currency_pair=f'{crypto_symbol}-USD')['amount']
    return float(crypto_price)

if __name__ == '__main__':
    app.run(debug=True)
