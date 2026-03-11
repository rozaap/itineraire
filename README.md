# Pause fraîcheur à Villeurbanne

Le projet "Pause fraîcheur à Villeurbanne" est un projet mené par des étudiants du master Géonum (Géographies Numériques) et du master Sentinelles, en partenariat avec la mairie de Villeurbanne.
L'objectif principal de ce projet est d'apporter une solution d'adaptation à la canicule en proposant une application avec 3 fonctionnalités principales :

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

Avant de lancer le code il est important de télécharger certaines données nécessaires au bon fonctionnement de l'application, et les mettre à leur place :

Ombres 8h: "backend\score_calculation_it\input_data\ombre\8h.tif"  
Ombres 13h: "backend\score_calculation_it\input_data\ombre\13h.tif"  
Ombres 18h: "backend\score_calculation_it\input_data\ombre\18h.tif"  
Temperature: "backend\score_calculation_it\input_data\Temperature\villeurbanne25_LST2024_DistTempMean_3946.tiff"  
Végétation stratifié: "backend\score_calculation_it\input_data\Vegetation_strat_Vlb\Vegetation_strat_vlb.shp"  
Mobilier urbain: "backend\score_calculation_it\input_data\Mobilier_urbain\Mobilierurbain.shp"  
Sanitaires: "backend\score_calculation_it\input_data\sanitaires\Sanitaires.shp"  
Parc: "backend\score_calculation_it\input_data\EV_EspaceVert\EV_EspaceVert.shp"  

Afin de lancer le code, se positionner à la racine du dossier backend et exécuter la commande suivante : 

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

### Le Script

Ce script permet de réaliser un graphe pondéré en fonction de plusieurs données présenté plus haut qui pourra être utilisé pour trouver le plus court
chemin en fonction des points frais de la ville de Villeurbanne.
Le script python principal du backend est le fichier **create_graph.py** qui constitue le *endpoint* du backend permettant d'exécuter le calcul de graphe. Avant le lancement du code, vérifier les chemins d'accès au données du fichier **global_variable.py**.

# Pondération du réseau piéton

## Pre-processing
Afin de pouvoir réaliser le calcul de la pondération, il est nécessaire de faire un pre-processing. Si les données sont amenées à être mises à jour, chaque script peut être exécutable pour relancer les calculs spécifiques à chaque donnée. En sortie de chaque script on obtient un sous-réseau enregistré dans un fichier **vil_network_bounding.gpkg** qui nous permet d'avoir le taux de recouvrement ou la présence d'une donnée sur chaque segments.

Ils correpondent à une version des données de la mairie de Villeurbanne au début de l'année 2026.

### Le réseau de Villeurbanne
Cette donnée est indispensable et à récupérer à partir d'OpenStreetMap et le fichier responsable de sa récupération est dans le fichier **fetch_network.py** à partir de *./score_calculation_it/input_data/*.

## Pondération du graphe (calcul du score)
La pondération du graphe ne peut se faire que si l'ensemble des sous-réseaux existent (et ont été mis à jour au besoin). La pondération du graphe est à renseigner directement dans le fichier **score_calculation.py**.

Pondération choisie : 
Arbres/arbuste = 8
Parc = 3
Ombre = 10
Température = 6
Eau (bornes fontaines, sanitaires) = 7
Banc, fontaines = 2


