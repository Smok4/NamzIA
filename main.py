import gym
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import requests

# Définir l'environnement d'investissement
class InvestmentEnvironment(gym.Env):
    def __init__(self):
        super(InvestmentEnvironment, self).__init__()
        self.observation_space = gym.spaces.Discrete(1)
        self.action_space = gym.spaces.Discrete(2)
        self.initial_balance = 1000
        self.current_balance = self.initial_balance
        self.goal_balance = 10000

    def step(self, action):
        if action == 0:  # Investir
            investment_return = np.random.uniform(0, 0.05) * self.current_balance
            self.current_balance += investment_return

        done = self.current_balance >= self.goal_balance
        reward = self.current_balance - self.initial_balance
        return 0, reward, done, {}

    def reset(self):
        self.current_balance = self.initial_balance
        return 0

# Définir l'agent DQN
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.model = self.build_model()
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
        self.target_model = self.build_model()
        self.target_update_counter = 0
        self.update_target_frequency = 100

    def build_model(self):
        model = tf.keras.Sequential([
            layers.Dense(24, activation='relu', input_shape=(self.state_size,)),
            layers.Dense(24, activation='relu'),
            layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=self.optimizer)
        return model

    def act(self, state):
        return np.argmax(self.model.predict(np.array(state).reshape(1, self.state_size)))

    def train(self, replay_buffer, batch_size=32, discount_rate=0.95):
        batch = replay_buffer.sample(batch_size)
        states, actions, rewards, next_states, dones = batch

        target_qs = self.target_model.predict(states)
        next_qs = self.target_model.predict(next_states)

        for i in range(batch_size):
            if dones[i]:
                target_qs[i][actions[i]] = rewards[i]
            else:
                target_qs[i][actions[i]] = rewards[i] + discount_rate * np.max(next_qs[i])

        self.model.fit(states, target_qs, batch_size=batch_size, verbose=0)

        self.target_update_counter += 1
        if self.target_update_counter >= self.update_target_frequency:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0

# Fonction pour envoyer de la crypto-monnaie à une adresse spécifique
def send_money_to_address(address, amount):
    # Simuler l'envoi de crypto-monnaie à l'aide d'une API de service tiers
    response = requests.post("https://api.example.com/send_money", json={"address": address, "amount": amount})
    if response.status_code == 200:
        print("Transaction réussie!")
    else:
        print("Échec de la transaction.")

# Paramètres d'apprentissage
state_size = 1
action_size = 2
batch_size = 32
discount_rate = 0.95

# Créer l'environnement et l'agent
env = InvestmentEnvironment()
agent = DQNAgent(state_size, action_size)

# Entraîner l'agent
num_episodes = 1000
for episode in range(num_episodes):
    state = env.reset()
    done = False
    while not done:
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        agent.train(replay_buffer=None, batch_size=batch_size, discount_rate=discount_rate)
        state = next_state

    # Envoyer de l'argent à l'adresse de crypto-monnaie après chaque épisode
    address = "YOURWALLET"  # Adresse de réception des jetons ATOM
    amount = env.current_balance  # Envoyer tout le solde actuel
    send_money_to_address(address, amount)
    print(f"Episode {episode + 1}/{num_episodes}, Total Balance: ${env.current_balance:.2f}")
