import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from coinbase.wallet.client import Client
import time

# Initialiser le client Coinbase avec vos informations d'identification
client = Client("YOUR_API_KEY", "YOUR_API_SECRET")

# Fonction pour récupérer le prix actuel du ATOM à partir de Coinbase
def get_atom_price():
    atom_price = client.get_buy_price(currency_pair='ATOM-USD')['amount']
    return float(atom_price)

# Classe pour l'environnement d'investissement
class InvestmentEnvironment:
    def __init__(self):
        self.atom_price = get_atom_price()
        self.balance = 1000  # Solde initial en USD

    def get_state(self):
        return np.array([self.atom_price])

    def step(self, action):
        # Logique pour effectuer des transactions réelles sur Coinbase
        pass

# Classe pour l'agent DQN
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.95  # Facteur de réduction
        self.epsilon = 1.0  # Exploration initiale
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = self.build_model()

    def build_model(self):
        model = tf.keras.Sequential([
            layers.Dense(24, activation='relu', input_shape=(self.state_size,)),
            layers.Dense(24, activation='relu'),
            layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001))
        return model

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(range(self.action_size))
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train(self, batch_size=32):
        if len(self.memory) < batch_size:
            return
        minibatch = np.random.choice(self.memory, batch_size, replace=False)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Paramètres d'apprentissage
state_size = 1
action_size = 2

# Créer l'environnement et l'agent
env = InvestmentEnvironment()
agent = DQNAgent(state_size, action_size)

# Boucle principale
num_episodes = 1000
batch_size = 32
for episode in range(num_episodes):
    state = env.get_state()
    done = False
    while not done:
        action = agent.act(state)
        next_state, reward, done = env.step(action)
        agent.remember(state, action, reward, next_state, done)
        state = next_state
    agent.train(batch_size)

    # Envoyer de l'argent à l'adresse de crypto-monnaie après chaque épisode
    # Remplacez `RECIPIENT_ADDRESS` par l'adresse du destinataire et `AMOUNT_TO_SEND` par le montant que vous souhaitez envoyer
    recipient_address = 'RECIPIENT_ADDRESS'
    amount = 'AMOUNT_TO_SEND'
    currency = 'ATOM'

    # Envoyer des fonds à l'adresse du destinataire
    transaction = client.send_money(
        'YOUR_ACCOUNT_ID',  # Remplacez par votre identifiant de compte Coinbase
        to=recipient_address,
        amount=amount,
        currency=currency
    )

    print(f"Transaction ID : {transaction.id}")
    print(f"Episode {episode + 1}/{num_episodes}, Total Balance: ${env.balance:.2f}")

    time.sleep(3600)  # Attendre 1 heure avant de vérifier à nouveau le prix du ATOM
