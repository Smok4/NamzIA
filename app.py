from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
from werkzeug.security import generate_password_hash, check_password_hash
import concurrent.futures
import stripe
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Remplacez par votre propre clé secrète

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configuration des clés Stripe
stripe_keys = {
    'secret_key': 'stripe secret key',  # Remplacez par votre clé secrète
    'publishable_key': 'stripe secret key'  # Remplacez par votre clé publique
}
stripe.api_key = stripe_keys['secret_key']

# Modèle de la base de données pour les utilisateurs
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  # 'admin' or 'user'

    def __init__(self, email, password, role='user'):
        self.email = email
        self.set_password(password)
        self.role = role

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

# Création de la base de données
with app.app_context():
    db.create_all()

# Initialize admin account if no users exist
    if User.query.count() == 0:
        admin = User(email='namz.pentest@gmail.com', password='1337guy$$$', role='admin')
        db.session.add(admin)
        db.session.commit()
        print("Admin account created with email 'admin@example.com' and password 'adminpassword'")


# Fonction pour obtenir les données de marché de plusieurs crypto-monnaies
def get_cryptos_data(crypto_symbols):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(crypto_symbols)}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Ajouter la récupération des valeurs ATH
        for crypto in crypto_symbols:
            ath_data = requests.get(f"https://api.coingecko.com/api/v3/coins/{crypto}").json()
            data[crypto]['ath'] = ath_data.get('market_data', {}).get('ath', {}).get('usd', 'N/A')
            data[crypto]['ath_change_percentage'] = ath_data.get('market_data', {}).get('ath_change_percentage', {}).get('usd', 'N/A')
    else:
        data = {}
    return data

# Fonction pour récupérer les symboles des crypto-monnaies du top 200 par capitalisation boursière
def get_top_200_crypto_symbols():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=200&page=1&sparkline=false"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        STABLECOINS = {'tether', 'usd-coin', 'binance-usd', 'dai', 'terrausd'}
        crypto_symbols = [crypto['id'] for crypto in data if crypto['id'] not in STABLECOINS]
    else:
        crypto_symbols = []
    return crypto_symbols

# Fonction pour calculer le RSI
def calculate_rsi(crypto):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart?vs_currency=usd&days=14"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        prices = [price[1] for price in data['prices']]
    else:
        prices = []

    gains = []
    losses = []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        if change > 0:
            gains.append(change)
        else:
            losses.append(abs(change))

    avg_gain = sum(gains) / len(gains) if gains else 0
    avg_loss = sum(losses) / len(losses) if losses else 0

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Fonction pour scraper le sentiment du marché
def get_market_sentiment(crypto_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    search_url = f"https://www.google.com/search?q={crypto_name}+crypto+market+sentiment"
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        return 0
    
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    positive_words = ['buy', 'bullish', 'positive', 'growth', 'up']
    negative_words = ['sell', 'bearish', 'negative', 'loss', 'down']
    positive_count = sum(text.count(word) for word in positive_words)
    negative_count = sum(text.count(word) for word in negative_words)

    sentiment_score = positive_count - negative_count
    return sentiment_score

# Fonction pour déterminer un classement des cryptos par potentiel
def get_crypto_rankings(crypto_data):
    rankings = []

    # Initialiser les valeurs minimales et maximales pour chaque métrique
    min_volume = max_volume = min_change = max_change = min_rsi = max_rsi = 0
    min_sentiment = max_sentiment = min_ath = max_ath = min_ath_change = max_ath_change = 0
    initialized = False

    # Parcourir les données pour trouver les valeurs minimales et maximales
    for data in crypto_data.values():
        if not data.get('usd_24h_vol'):
            continue

        volume = float(data.get('usd_24h_vol', 0.0))
        change = float(data.get('usd_24h_change', 0.0))
        rsi = float(data.get('rsi', 0.0))
        sentiment = float(data.get('sentiment', 0.0))

        try:
            ath = float(data.get('ath', 0.0))
        except ValueError:
            ath = 0.0

        try:
            ath_change = float(data.get('ath_change_percentage', 0.0))
        except ValueError:
            ath_change = 0.0

        if not initialized:
            min_volume = max_volume = volume
            min_change = max_change = change
            min_rsi = max_rsi = rsi
            min_sentiment = max_sentiment = sentiment
            min_ath = max_ath = ath
            min_ath_change = max_ath_change = ath_change
            initialized = True
        else:
            min_volume = min(min_volume, volume)
            max_volume = max(max_volume, volume)
            min_change = min(min_change, change)
            max_change = max(max_change, change)
            min_rsi = min(min_rsi, rsi)
            max_rsi = max(max_rsi, rsi)
            min_sentiment = min(min_sentiment, sentiment)
            max_sentiment = max(max_sentiment, sentiment)
            min_ath = min(min_ath, ath)
            max_ath = max(max_ath, ath)
            min_ath_change = min(min_ath_change, ath_change)
            max_ath_change = max(max_ath_change, ath_change)

    # Normaliser les scores et calculer le score total
    for crypto, data in crypto_data.items():
        if not data.get('usd_24h_vol'):
            continue

        volume_score = normalize(float(data.get('usd_24h_vol', 0.0)), min_volume, max_volume)
        change_score = normalize(float(data.get('usd_24h_change', 0.0)), min_change, max_change)
        rsi_score = normalize(float(data.get('rsi', 0.0)), min_rsi, max_rsi)
        sentiment_score = normalize(float(data.get('sentiment', 0.0)), min_sentiment, max_sentiment)

        try:
            ath_score = normalize(float(data.get('ath', 0.0)), min_ath, max_ath)
        except ValueError:
            ath_score = 0.0

        try:
            ath_change_percentage = normalize(float(data.get('ath_change_percentage', 0.0)), min_ath_change, max_ath_change)
        except ValueError:
            ath_change_percentage = 0.0

        total_score = (volume_score + change_score + rsi_score + sentiment_score + ath_score + ath_change_percentage) / 6  # Moyenne des scores

        rankings.append((crypto, total_score, data))

    rankings.sort(key=lambda x: x[1], reverse=True)  # Trier par score total décroissant

    return rankings


    # Normaliser les scores et calculer le score total
    for crypto, data in crypto_data.items():
        if not data.get('usd_24h_vol'):
            continue

        volume_score = normalize(float(data.get('usd_24h_vol', 0.0)), min_volume, max_volume)
        change_score = normalize(float(data.get('usd_24h_change', 0.0)), min_change, max_change)
        rsi_score = normalize(float(data.get('rsi', 0.0)), min_rsi, max_rsi)
        sentiment_score = normalize(float(data.get('sentiment', 0.0)), min_sentiment, max_sentiment)
        ath_score = normalize(float(data.get('ath', 0.0)), min_ath, max_ath)
        ath_change_percentage = normalize(float(data.get('ath_change_percentage', 0.0)), min_ath_change, max_ath_change)

        total_score = (volume_score + change_score + rsi_score + sentiment_score + ath_score + ath_change_percentage) / 6  # Moyenne des scores

        rankings.append((crypto, total_score, data))

    rankings.sort(key=lambda x: x[1], reverse=True)  # Trier par score total décroissant

    return rankings

# Fonction pour normaliser les valeurs
def normalize(value, min_value, max_value):
    if max_value == min_value:
        return 0
    return (value - min_value) / (max_value - min_value)
    
def to_float(value):
    try:
        return float(value)
    except ValueError:
        return 0.0

app.jinja_env.filters['to_float'] = to_float

# Route de la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

# Route pour afficher les données des crypto-monnaies
@app.route('/cryptos')
def cryptos():
    crypto_symbols = get_top_200_crypto_symbols()
    crypto_data = get_cryptos_data(crypto_symbols)
    return render_template('cryptos.html', crypto_data=crypto_data)

# Route pour le bouton "Start" qui lance le bot
@app.route('/start_bot')
def start_bot():
    crypto_symbols = get_top_200_crypto_symbols()[:200]  # Analyser seulement le top 200 pour la vitesse
    crypto_data = get_cryptos_data(crypto_symbols)

    def enrich_crypto_data(crypto):
        data = crypto_data.get(crypto, {})
        data['rsi'] = calculate_rsi(crypto)
        data['sentiment'] = get_market_sentiment(crypto)
        crypto_data[crypto] = data

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(enrich_crypto_data, crypto_symbols)

    rankings = get_crypto_rankings(crypto_data)

    # Enregistrer les classements dans un fichier .txt
    with open('crypto_rankings.txt', 'w') as file:
        for rank, (crypto, score, data) in enumerate(rankings, start=1):
            file.write(f"{rank}. {crypto} - Score: {score}\n")
            file.write(f"    Volume de trading: {data.get('usd_24h_vol', 'N/A')}\n")
            file.write(f"    Pourcentage de changement sur 24 heures: {data.get('usd_24h_change', 'N/A')}\n")
            file.write(f"    RSI: {data.get('rsi', 'N/A')}\n")
            file.write(f"    Sentiment du marché: {data.get('sentiment', 'N/A')}\n")
            file.write(f"    ATH: {data.get('ath', 'N/A')}\n")
            file.write(f"    Pourcentage de changement ATH: {data.get('ath_change_percentage', 'N/A')}\n")
            file.write("\n")

    return render_template('bot_result.html', rankings=rankings, enumerate=enumerate)

# Page de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # Login successful
            return redirect(url_for('home'))
        flash('Invalid email or password')
    return render_template('login.html')

# Page d'enregistrement
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        subscription_type = request.form['subscription_type']

        if User.query.filter_by(email=email).first():
            return 'Email already registered'

        # Redirect to Stripe Checkout
        return redirect(url_for('create_checkout_session', email=email, password=password, subscription_type=subscription_type))
    return render_template('register.html', stripe_keys=stripe_keys)

# Route for creating Stripe Checkout Session
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    email = request.form['email']
    password = request.form['password']
    subscription_type = request.form['subscription_type']

    prices = {
        'monthly': 'price_1PLPvTIdYFjfRFy5FX0GhZsR',   # Remplacez par vos identifiants de prix réels
        'quarterly': 'price_1HxXlI2eZvKYlo2C4PmK92r7',
        'yearly': 'price_1HxXlI2eZvKYlo2CbZQJyr4u'
    }

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': prices[subscription_type],
                'quantity': 1,
            }],
            mode='subscription',
            success_url=url_for('payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}&email=' + email + '&password=' + password + '&subscription_type=' + subscription_type,
            cancel_url=url_for('payment_cancel', _external=True),
        )
        return jsonify({'id': session['id']})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/payment-success')
def payment_success():
    session_id = request.args.get('session_id')
    email = request.args.get('email')
    password = request.args.get('password')
    subscription_type = request.args.get('subscription_type')

    if not session_id:
        return 'Session ID not found', 400

    session = stripe.checkout.Session.retrieve(session_id)
    if not session or session.payment_status != 'paid':
        return 'Payment failed', 400

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(email=email, password=hashed_password, subscription_type=subscription_type)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/payment-cancel')
def payment_cancel():
    return 'Payment was canceled', 400

# Page de support
@app.route('/support')
def support():
    return render_template('support.html')

# Route pour afficher le panneau d'administration
@app.route('/admin')
def admin():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    user = User.query.filter_by(email=session['user_email']).first()
    if user.subscription_type != 'admin':
        return 'Access denied', 403

    users = User.query.all()
    return render_template('admin.html', users=users)

# Route pour la déconnexion
@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
