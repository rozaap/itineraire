import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import os
from data_utils import *
import sys
sys.path.append("../")
#from global_variable import *

###### CREATE WORKING DIRECTORY FOR PARCS ET JARDINS ######
create_folder("backend/score_calculation_it/output_data/Sanitaire/")
sanitaire_path = "backend/score_calculation_it/input_data/sanitaires/Sanitaires.shp"
edges_buffer_path = "backend/score_calculation_it/input_data/vil_network_bounding.gpkg"
vil_area_path = "backend/score_calculation_it/input_data/villeurbanne/villeurbanne.shp"
network_sanitaire = "backend/score_calculation_it/output_data/Sanitaire/network_Sanitaire.gpkg"

choice = 'OUI'#input("""
   # Souhaitez-vous mettre à jour le réseau pondéré par les parcs ? OUI ou NON
#""")
if(choice=="OUI"):
    sanitaire = gpd.read_file(sanitaire_path)
    network = gpd.read_file(edges_buffer_path, layer="edges_buffer")

    if network.crs != sanitaire.crs:
        sanitaire = sanitaire.to_crs(network.crs)

    # Spatial join
    joined = gpd.sjoin(network, sanitaire, how="left", predicate="intersects")

    # On garde uniquement les vraies intersections
    intersections = joined[joined["index_right"].notna()]

    # Récupérer les index du network concernés
    idx = intersections.index.unique()

    # Ajouter colonne au network
    network["sanitaire_present"] = 0
    network.loc[idx, "sanitaire_present"] = 1

    # Sauvegarder
    network.to_file(network_sanitaire, driver="GPKG")
