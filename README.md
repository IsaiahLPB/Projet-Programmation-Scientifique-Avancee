# Projet_PSA
### Simon Darnault, Arnault Marquis, Emre Onal

## Préparer l'environnement
Ce projet utilise MongoDC pour stocker les données en local sur la machine. L'utilisateur doit installer MongoDB avant de lancer des calculs. La procédure pour l'installation est décrite sur [ce site](https://www.mongodb.com/docs/manual/administration/install-community/).

### La base de donnée
Exécuter les commandes suivantes, une fois la base de donnée téléchargée.
- ```systemctl start mongod.service```
- ```mongosh mongodb://127.0.0.1```
- ```use results```
- ```db.createUser({ user: "user0", pwd: "pwd0", roles: ["dbAdmin"]})```

Pour afficher les différentes expériences dans la base de donée
- ```db.experienceName.find()```

À la racine du projet utilisez la commande `make init` pour créer un environnement virtuel pour Python. Cela créra l'environnement virtuel et chargera les modules nécessaires au bon déroulement du projet. Cette commande crée ensuite les bindings Python, qui permettent d'appeler des fonctions C++ depuis un programme Python.

Dans un premier temps, modifiez le fichier *consts.JSON* à la racine du projet pour modifier les paramètres de l'expérience que vous souhaitez réaliser.

## Préparer un expérience
Le champs **V** doit correspondre à une entrée parmi : **Harmonic**, **Null** et **Image**, qui permettent de créer respectivement, un poteniel harmonique, un nul et de définir le potentiel à partir d'une image en niveau de gris.

Le champs **image_V** doit correspondre au nom de l'image souhaité. Les images doit être stockée dans le dossier *images* à la racine. Deux images sont déjà disponible dans le dossier.

## Lancer une expérience
Ensuite, entrez la commande `make exp` pour commencer l'expérience paramétrée dans le fichier JSON.