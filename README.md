# Projet d'IA d'Investissement

Ce projet vise à développer une intelligence artificielle (IA) capable de prendre des décisions d'investissement intelligentes dans un environnement simulé. L'IA utilise des techniques d'apprentissage par renforcement avancées pour maximiser ses gains financiers et envoie périodiquement ses gains à une adresse de crypto-monnaie spécifique.

## Fonctionnalités

- Utilisation de l'algorithme Deep Q-Network (DQN) pour l'apprentissage par renforcement.
- Interaction avec un environnement d'investissement simulé.
- Envoi de gains financiers à une adresse de crypto-monnaie spécifique à l'aide d'une API de service tiers.

## Comment ça marche

L'IA est représentée par un agent qui interagit avec un environnement d'investissement simulé. À chaque étape, l'agent choisit une action (investir ou ne pas investir) en fonction de son estimation actuelle des valeurs Q, qui représentent les récompenses attendues pour chaque action dans chaque état. L'agent est entraîné sur plusieurs épisodes d'interaction avec l'environnement pour améliorer ses décisions d'investissement au fil du temps.

Après chaque épisode, l'IA envoie le solde financier actuel à une adresse de crypto-monnaie spécifique à l'aide d'une fonction `send_money_to_address`. Cette fonction simule l'envoi de crypto-monnaie à l'aide d'une API de service tiers.

## Configuration requise

- Python 3.x
- TensorFlow
- Gym

## Utilisation

1. Cloner ce dépôt sur votre machine locale.
2. Installer les dépendances requises : `pip install -r requirements.txt`.
3. Exécuter le script principal : `python main.py`.

## Auteur

Namz

## Licence

Ce projet est sous licence NamzDev™. Voir le fichier LICENSE.md pour plus de détails.

