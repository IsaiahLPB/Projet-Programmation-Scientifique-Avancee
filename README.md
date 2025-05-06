# Projet_PSA
### Simon Darnault, Arnault Marquis, Emre Onal

## Préparer l'environnement
À la racine du projet utilisez la commande `make venv` pour créer un environnement virtuel pour Python. Cela créra l'environnement virtuel et chargera les modules nécessaires au bon déroulement du projet.

Ce projet utilise MongoDC pour stocker les données en local sur la machine. L'utilisateur doit installer MongoDB avant de lancer des calculs. La procédure pour l'installation est décrite sur [ce site](https://www.mongodb.com/docs/manual/administration/install-community/).

## Compiler le projet avec les bindings Python
Pour bien compiler le projet sur votre machine entrez `make bindings` pour compiler l'ensemble du projet.

Il existe aussi une commande `make init` qui fera l'ensemble des commandes `make venv` et `make bindings` en une seule fois.

## Lancer une expérience
Dans un premier temps, modifiez le fichier `consts.JSON` à la racine du projet pour modifier les paramètres de l'expérience que vous souhaitez réaliser.

Ensuite, entrez la commande `make exp` pour commencer l'expérience paramétrée dans le fichier JSON.