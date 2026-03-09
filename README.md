# Pause fraîcheur à Villeurbanne

---

# Table des matières

- [À propos](#à-propos)
- [Pré-requis](#pré-requis)
- [Application web](#application-web)
    - [Backend](#backend)
    - [Frontend](#frontend)
- [Analyse statistique : pondération du réseau piéton](#analyse-statistique--pondération-du-réseau-piéton)


# 🚀 Démarrage rapide

copier le fichier **.env.example** et le renommer en **.env** à la racine du projet. 
```bash
cp .env.example .env
```

télécharger les data de opendata lyon
```bash
cd score_calculation_it/input_data
pip i geopandas owslib
python fetch_data.py
# Selectionner l'option WEB_ONLY
```

lancer le backend et le frontend
```bash
docker-compose up
```

Le frontend est accessible à l'adresse [http://localhost:3000](http://localhost:3000)
Le backend est accessible à l'adresse [http://localhost:3002](http://localhost:3002)



# À propos

Le projet "Pause fraîcheur à Villeurbanne est un projet mené par des étudiants du master Géonum (Géographies Numériques) de deuxième année, en partenariat avec la mairie de Villeurbanne.
L'objectif principal de ce projet est d'apporter une solution d'adaptation à la canicule en proposant une application avec 3 fonctionnalitées principales :

- Trouver les lieux "frais" autour de chez soi
- Afficher des éléments utiles en cas de canicule (fontaines, parcs, toilettes etc.)
- Proposer des itinéraires piétons permettant de se déplacer "au frais", en minimisant la chaleur le long du trajet

Le code à été inspiré par le projet "Parcours à la carte" aussi appelé "Sortons au frais", réalisé par Erasme (laboratoire d'innovation de la Métropole de Lyon), le service Données Métropolitaines et le service Géomatique de la Métropole de Lyon.
[https://datagora.erasme.org/projets/sortons-au-frais/](https://datagora.erasme.org/projets/sortons-au-frais/)
La pondération du réseau piéton a été expliqué dans un rapport livré à la mairie.


# Pré-requis et Installation

Le projet a été développé sur python 12.0
La liste des librairie nécessaires est dans le fichier "requirement.txt"

## Exécution

### Création de l'environnement conda

Une fois conda installé (via anaconda par exemple), se placer à la racine du projet et créer un environnement conda pour le projet via la commande suivante : 

```bash
conda create --name <nom-env>
```
Suivre les indications de créations de l'environnement puis une fois à la racine du projet, activer l'environnement conda : 

```bash
conda activate <nom-env>
```

Puis installer toutes les dépendances avec 

```bash
pip install -r requirements.txt
```

## Exécution du code
**Se placer à la racine du dossier backend**

Avant de lancer le code il est important de télécharger certaines données nécessaires au bon fonctionnement de l'application, et les mettre à leur place

Afin de lancer le backend, se positionner à la racine du dossier backend et exécuter la commande suivante : 

```bash
python create_graph.py
```

# Application web

## Backend

Toutes les variables globales (les chemins des fichiers, les paramètres spécifiques etc.) sont stockées dans le fichier **global_variable.py** à la racine du dossier backend. Il n'y a pas de base de données pour ce projet car il n'y en avait pas le besoin.

### LES DONNÉES 
L'ensemble des données utiles pour le calcul de graphe et des score sont stockées dans le dossier *score_calculation_it/input_data*

On peut distinguer trois types de données : 

- Les données issus de la mairie de Villeurbanne
- Les données issus d'OpenStreetMap
- les données d'ombre issues de ShadeMap


### L'API
Le script python principal du backend est le fichier **create_graph.py** qui constitue le *endpoint* du backend permettant d'exécuter le calcul de graphe. Avant le lancement du code, vérifier les chemins d'accès au données du fichier **global_variable.py**.

# Pondération du réseau piéton et analyse statistique

## Pre-processing
Afin de pouvoir réaliser le calcul de la pondération, il est nécessaire de faire un pre-processing. Si les données sont amenées à être mise à jour, chaque script peut être exécutable pour relancer les calculs spécifiques à chaque donnée. En sortie de chaque script on obtient un sous-réseau enregistré dans un fichier **edges_nom_données.gpkg** qui nous permet d'avoir le taux de recouvrement ou la présence d'une donnée sur chaque segments.

Ils correpondent à une version des données de la mairie de Villeurbanne au début de l'année 2026.

### Le réseau de Villeurbanne
Cette donnée est indispensable pour la suite (à télécharger en premier lieu donc). Afin de la mettre à jour, exécuter le fichier 
**fetch_network.py** à partir de *./score_calculation_it/input_data/* et se laisser guider par les instructions du terminal.

```bash
python fetch_network.py
```

### Le mobilier urbain
Actuellement les points d'interêts (POI) ne sont pas pris en compte dans la pondération du graphe, cependant, il existe un fichier **poi_preprocessing.py** permettant de calculer la présence de POI sur les segments. Les résultats pourraient être utilisés dans le cadre d'une amélioration du calculateur d'itinéraire. 


### Parcs et Jardins
Les parcs ont un traitement un peu différents des autres POI, par conséquent, les calculs nécessaire pour le calculateur d'itinéraire peuvent être exécuté via le fichier **parcs_jardins_preprocessing.py**.

### Eaux
Les cours d'eau ont un traitement un peu différents des autres POI, par conséquent, les calculs nécessaire pour le calculateur d'itinéraire peuvent être exécuté via le fichier **eaux_preprocessing.py** et en se laissant guider par les instructions du terminal.

### La végétation
La donnée de végétation stratifiée la donnée la plus volumineuse.

### La température

### L'ombre 

## Pondération du graph (calcul du score)
La pondération du graph ne peut se faire que si l'ensemble des sous-réseaux existent (et ont été mis à jour au besoin). La pondération du graph est à renseigner directement dans le fichier **score_calculation.py**.

