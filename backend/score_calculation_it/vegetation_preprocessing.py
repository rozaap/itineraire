import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import os
from data_utils import *
import sys
sys.path.append("../")
#Appel des données
from global_variable import *

###### CREATE WORKING DIRECTORY FOR VEGETATION #######
create_folder("backend/score_calculation_it/output_data/vegetation_strat/")

###### VEGETATION PREPROCESSING ######
"""Les données proviennent de la mairie de Villeurbanne """

### SCRIPT ###
# Ce script permet de calculer le pourcentage de végatation sur chaque différents segments de la ville

###### VEGETATION STRATIFIEE PREPROCESSING ######
def vegetation():
    vegetation = gpd.read_file(vegetation_path)
    network = gpd.read_file(vil_network_bounding_path, layer="edges_buffer")

    # Vérification de la projection
    if network.crs != vegetation.crs:
        vegetation = vegetation.to_crs(network.crs)

    # Ajouter d'un ID unique
    network = network.reset_index(drop=True)
    network["net_id"] = network.index

    # Calcul des surfaces
    network["area_total"] = network.geometry.area

    # Intersection 
    intersection = gpd.overlay(network, vegetation, how="intersection")

    # Surface intersectée
    intersection["area_inter"] = intersection.geometry.area

    # Somme des surfaces par polygone réseau
    area_sum = (
        intersection.groupby("net_id")["area_inter"]
        .sum()
    )

    # Calcul du poucentage de végétation
    network["pct_vegetation"] = (
       network["net_id"].map(area_sum) / network["area_total"]*100
    )

    network["pct_vegetation"] = network["pct_vegetation"].fillna(0)
    
    # Sauvegarder
    network.to_file(network_vegetation_path, driver="GPKG")

vegetation()