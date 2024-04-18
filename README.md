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

---

## Comment trouver votre API Key et API Secret sur Coinbase

1. Connectez-vous à votre compte Coinbase sur [coinbase.com](https://www.coinbase.com/).

2. Dans le menu de navigation, cliquez sur votre profil dans le coin supérieur droit, puis sélectionnez "API".

3. Si vous n'avez pas encore créé de clé API, cliquez sur "Créer une clé API". Sinon, vous verrez une liste de vos clés API existantes.

4. Pour créer une nouvelle clé API, cliquez sur "Nouvelle clé API" et suivez les étapes pour configurer vos autorisations et vos paramètres de sécurité. Vous devrez peut-être fournir votre mot de passe Coinbase pour confirmer la création de la clé API.

5. Une fois que votre clé API est créée, vous verrez votre clé API et votre secret API. **Notez bien votre secret API car il ne sera affiché qu'une seule fois.** Assurez-vous de le copier dans un endroit sûr et ne le partagez avec personne.

6. Vous pouvez maintenant utiliser votre clé API et votre secret API dans votre application ou votre projet.

---

N'oubliez pas de remplacer les instructions génériques par des captures d'écran ou des exemples spécifiques si vous le jugez nécessaire pour rendre le tutoriel plus clair pour vos utilisateurs.

## Auteur

Namz

## Licence

Ce projet est sous licence NamzDev™. Voir le fichier LICENSE.md pour plus de détails.

