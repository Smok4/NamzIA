

# Agent d'Investissement Intelligent

Ce projet consiste en un agent d'investissement intelligent qui prend des décisions d'achat et de vente de crypto-monnaies en fonction des fluctuations du marché. L'agent utilise l'apprentissage par renforcement pour apprendre à maximiser les bénéfices tout en minimisant les pertes.

## Objectif

L'objectif principal de ce projet est de développer un système d'investissement automatisé capable de prendre des décisions éclairées sur les transactions de crypto-monnaies. L'agent doit être capable d'apprendre et d'adapter ses stratégies en fonction des changements du marché.

## Fonctionnalités

- Surveillance en temps réel du prix des crypto-monnaies à partir de sources telles que Coinbase.
- Prise de décision d'achat et de vente basée sur des seuils prédéfinis et des stratégies d'investissement.
- Utilisation de l'apprentissage par renforcement pour améliorer les performances de l'agent au fil du temps.
- Intégration avec l'API Coinbase pour effectuer des transactions réelles sur le marché.

## Architecture

Le projet est construit autour de plusieurs composants principaux :

1. **Environnement d'Investissement :** L'IA est sur le marché des crypto-monnaies grace à Coinbase et fournit des informations sur les prix et les actions à prendre.
2. **Agent d'Investissement :** Utilise un réseau neuronal pour prendre des décisions d'achat et de vente en fonction des observations de l'environnement.
3. **Intégration Coinbase :** Utilise l'API Coinbase pour effectuer des transactions réelles sur le marché.

## Développement Futur

Dans le cadre du développement futur, nous prévoyons d'ajouter les fonctionnalités suivantes :

- Amélioration de la précision des prédictions en utilisant des modèles d'apprentissage plus avancés.
- Intégration avec d'autres plateformes d'échange de crypto-monnaies pour une plus grande diversification des transactions.
- Implémentation de mécanismes de gestion des risques pour minimiser les pertes potentielles.

## Le Setup

1. Clés d'API Coinbase : Remplacez "YOUR_API_KEY" et "YOUR_API_SECRET" par vos propres clés d'API Coinbase.
2. ID du compte Coinbase : Remplacez 'YOUR_ACCOUNT_ID' par l'ID de votre compte Coinbase. Vous pouvez trouver cet ID en suivant les étapes mentionnées précédemment.
3. Adresse du destinataire et montant à envoyer : Dans la boucle principale du script, il y a une partie qui envoie de l'argent à une adresse de crypto-monnaie après chaque épisode. Vous devez remplacer
4. "RECIPIENT_ADDRESS" par l'adresse du destinataire et "AMOUNT_TO_SEND" par le montant que vous souhaitez envoyer.
5. Attente avant de vérifier le prix du ATOM : Dans la boucle principale du script, il y a une pause de 3600 secondes (1 heure) avant de vérifier à nouveau le prix du ATOM. Vous pouvez ajuster cette valeur en fonction de vos préférences.
6. Gestion des frais de transaction : Si vous le souhaitez, vous pouvez également ajuster la logique d'achat et de vente pour tenir compte des frais de transaction spécifiques à votre compte Coinbase.


## Comment trouver votre API Key et API Secret sur Coinbase

1. Connectez-vous à votre compte Coinbase sur [https://portal.cloud.coinbase.com/]((https://portal.cloud.coinbase.com/)).

2. Dans le menu de navigation, cliquez sur votre profil dans le coin supérieur droit, puis sélectionnez "API".

3. Si vous n'avez pas encore créé de clé API, cliquez sur "Créer une clé API". Sinon, vous verrez une liste de vos clés API existantes.

4. Pour créer une nouvelle clé API, cliquez sur "Nouvelle clé API" et suivez les étapes pour configurer vos autorisations et vos paramètres de sécurité. Vous devrez peut-être fournir votre mot de passe Coinbase pour confirmer la création de la clé API.

5. Une fois que votre clé API est créée, vous verrez votre clé API et votre secret API. **Notez bien votre secret API car il ne sera affiché qu'une seule fois.** Assurez-vous de le copier dans un endroit sûr et ne le partagez avec personne.

6. Vous pouvez maintenant utiliser votre clé API et votre secret API dans votre application ou votre projet.

## Trouvé son ID Coinbase

Pour trouver l'ID de votre compte Coinbase, vous pouvez suivre ces étapes :

1. Connectez-vous à votre compte Coinbase sur le site web : [coinbase.com](https://www.coinbase.com/).
2. Cliquez sur votre profil dans le coin supérieur droit de la page.
3. Dans le menu déroulant, sélectionnez "Paramètres".
4. Sous l'onglet "Comptes", vous devriez voir une liste de tous vos comptes, y compris votre compte en USD, EUR, BTC, etc.
5. Cliquez sur le compte pour lequel vous souhaitez obtenir l'ID.
6. Vous verrez maintenant une URL dans votre navigateur, qui ressemblera à quelque chose comme ceci : `https://www.coinbase.com/accounts/XXXXXXXX`. L'ID de compte est représenté par "XXXXXXXX" dans cette URL.

Notez que chaque devise aura son propre ID de compte. Assurez-vous de copier l'ID du compte que vous souhaitez utiliser dans votre script Python pour effectuer des opérations spécifiques.

---

## Contributions

Les contributions au projet sont les bienvenues ! Vous pouvez contribuer en proposant des améliorations, en signalant des problèmes ou en ouvrant des pull requests.
Donation pour les âmes charitable voulant aidé financièrement le projet (OSMOSIS) :  osmo1t6q4jm2sgusjm2j26k79gugyfqlw0qu9p66dwc

## Auteur

Namz

## Licence

Ce projet est sous licence NamzDev™. Voir le fichier LICENSE.md pour plus de détails.

