import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import os
from data_utils import *
import sys
sys.path.append("../")
#Appel des données
from global_variable import *

###### CREATE WORKING DIRECTORY FOR PARCS ET JARDINS ######
create_folder("backend/score_calculation_it/output_data/EspaceVert/")

###### PARC PREPROCESSING ######
"""Les données proviennent de la mairie de Villeurbanne """

### SCRIPT ###
# Ce script permet de vérifier la présence ou non des parcs différents segments de la ville


def parc():
    espacevert = gpd.read_file(espacevert_path)
    network = gpd.read_file(vil_network_bounding_path, layer="edges_buffer")

    if network.crs != espacevert.crs:
        espacevert = espacevert.to_crs(network.crs)

    # Spatial join
    joined = gpd.sjoin(network, espacevert, how="left", predicate="intersects")

    # On garde uniquement les vraies intersections
    intersections = joined[joined["index_right"].notna()]

    # Récupérer les index du network concernés
    idx = intersections.index.unique()

    # Ajouter colonne au réseau
    network["parc_present"] = 0
    network.loc[idx, "parc_present"] = 1

    # Sauvegarder
    network.to_file(network_espacevert_path, driver="GPKG")

parc()