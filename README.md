# Projet_PSA  
### Simon Darnault, Arnault Marquis, Emre Onal

## Préparer l'environnement  
Ce projet utilise MongoDB pour stocker les données en local sur la machine. L'utilisateur doit installer MongoDB avant de lancer des calculs. La procédure pour l'installation est décrite sur [ce site](https://www.mongodb.com/docs/manual/administration/install-community/).

### La base de données  
Exécuter les commandes suivantes, une fois la base de données téléchargée :  
- ```systemctl start mongod.service```  
- ```mongosh mongodb://127.0.0.1```  
- ```use results```  
- ```db.createUser({ user: "user0", pwd: "pwd0", roles: ["dbAdmin"]})```

Pour afficher les différentes expériences dans la base de données :  
- ```db.experienceName.find()```

À la racine du projet, utilisez la commande `make init` pour créer un environnement virtuel pour Python. Cela créera l'environnement virtuel et chargera les modules nécessaires au bon déroulement du projet. Cette commande crée ensuite les bindings Python, qui permettent d'appeler des fonctions C++ depuis un programme Python.

Dans un premier temps, modifiez le fichier *consts.JSON* à la racine du projet pour modifier les paramètres de l'expérience que vous souhaitez réaliser.

## Préparer une expérience  
Le champ **V** doit correspondre à une entrée parmi : **Harmonic**, **Null** et **Image**, qui permettent de créer respectivement un potentiel harmonique, un nul et de définir le potentiel à partir d'une image en niveaux de gris.

Le champ **image_V** doit correspondre au nom de l'image souhaitée. Les images doivent être stockées dans le dossier *images* à la racine. Deux images sont déjà disponibles dans le dossier.

Le champ **type** pour **psi** doit correspondre à une des trois entrées suivantes : **Gaussian** pour simuler une vague gaussienne, **2D-H0** pour simuler une solution d'un oscillateur harmonique ou **2DH0-mult** pour une combinaison de solutions d'oscillateur harmonique.

## Lancer une expérience  
Ensuite, entrez la commande `make exp` pour commencer l'expérience paramétrée dans le fichier JSON. Cela lance les trois modules de notre projet à la suite :

À savoir :  
- **Le field generator** qui permet d'initialiser une expérience et la base de données  
- **Le solveur** qui calcule les différentes matrices et les écrit dans la base de données  
- **Le post processor** qui crée les fichiers VTK des matrices d'une expérience sauvegardée dans la base de données

Il est aussi possible de lancer chaque module indépendamment avec :  
- ```make field_generator```  
- ```make solver```  
- ```make post_processor```

## Visualiser les résultats  
Pour visualiser les résultats, vous pouvez utiliser [Paraview](https://www.paraview.org/download/) et y charger les fichiers VTK.
