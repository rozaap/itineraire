import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import os
from data_utils import *
import sys
sys.path.append("../")
#from global_variable import *

###### CREATE WORKING DIRECTORY FOR PARCS ET JARDINS ######
create_folder("backend/score_calculation_it/output_data/EspaceVert/")
espacevert_path = "backend/score_calculation_it/input_data/EV_EspaceVert/EV_EspaceVert.shp"
edges_buffer_path = "backend/score_calculation_it/input_data/vil_network_bounding_buffer.gpkg"
vil_area_path = "backend/score_calculation_it/input_data/villeurbanne/villeurbanne.shp"
network_espacevert = "backend/score_calculation_it/output_data/EspaceVert/network_EspaceVert.gpkg"

choice = 'OUI'#input("""
   # Souhaitez-vous mettre à jour le réseau pondéré par les parcs ? OUI ou NON
#""")
if(choice=="OUI"):
    espacevert = gpd.read_file(espacevert_path)
    network = gpd.read_file(edges_buffer_path, layer="edges_buffer")

    if network.crs != espacevert.crs:
        espacevert = espacevert.to_crs(network.crs)

    # Spatial join
    joined = gpd.sjoin(network, espacevert, how="left", predicate="intersects")

    # On garde uniquement les vraies intersections
    intersections = joined[joined["index_right"].notna()]

    # Récupérer les index du network concernés
    idx = intersections.index.unique()

    # Ajouter colonne au network
    network["parc_present"] = 0
    network.loc[idx, "parc_present"] = 1

    # Sauvegarder
    network.to_file(network_espacevert, driver="GPKG")
