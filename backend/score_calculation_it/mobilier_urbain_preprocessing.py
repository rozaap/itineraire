import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
from data_utils import *
import sys
sys.path.append("../")
#from global_variable import *

### CREATE WORKING DIRECTORY ###
create_folder("./output_data/mobilier_urbain/")
mob_urbain_path = "backend/score_calculation_it/input_data/Mobilier_urbain/Mobilierurbain.shp"
edges_buffer_path = "backend/score_calculation_it/input_data/vil_network_bounding.gpkg"
vil_area_path = "backend/score_calculation_it/input_data/villeurbanne/villeurbanne.shp"
network_mob_urb = "backend/score_calculation_it/output_data/mobilier_urbain/network_mobilier_urbain.gpkg"

###### EAUX PREPROCESSING ######
"""Les données proviennent de la mairie de Villeurbanne"""

### SCRIPT ###
choice = input("""
#    Souhaitez-vous mettre à jour le réseau pondéré par le mobilier urbain ? OUI ou NON
#""")

if (choice =="OUI"):
    mob_urbain = gpd.read_file(mob_urbain_path)
    network = gpd.read_file(edges_buffer_path, layer="edges_buffer")

    if network.crs != mob_urbain.crs:
        mob_urbain = mob_urbain.to_crs(network.crs)

    # Spatial join
    joined = gpd.sjoin(network, mob_urbain, how="left", predicate="intersects")

    # Liste des types uniques
    types = mob_urbain["type_mobil"].dropna().unique()

    for t in types:
        # Polygones qui contiennent ce type
        mask = joined[joined["type_mobil"] == t]
        idx = mask.index.unique()
    
        col_name = f"has_{t}"
        network[col_name] = 0
        network.loc[idx, col_name] = 1

    # Sauvegarder
    network.to_file(network_mob_urb, driver="GPKG")

    
    