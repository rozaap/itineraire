import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
from data_utils import *
import sys
sys.path.append("../")
#Appel des données
from global_variable import *

### CREATE WORKING DIRECTORY ###
create_folder("./output_data/mobilier_urbain/")

###### MOBILIER URBAIN PREPROCESSING ######
"""Les données proviennent de la mairie de Villeurbanne pour les mobiliers urbains présent dans les parcs
   Les données en dehors de parc proviennent d'OpenStreetMap"""

### SCRIPT ###
# Ce script permet de vérifier la présence ou non des mobiliers urbains sur les différents segments de la ville

def mob_urbain():
    mob_urbain = gpd.read_file(mob_urbain_path)
    network = gpd.read_file(vil_network_bounding_path, layer="edges_buffer")

    #Verification des projections (EPSG:3946)
    if network.crs != mob_urbain.crs:
        mob_urbain = mob_urbain.to_crs(network.crs)

    # Spatial join
    joined = gpd.sjoin(network, mob_urbain, how="left", predicate="intersects")

    # Liste des différents mobiliers urbains
    types = mob_urbain["type_mobil"].dropna().unique()

    for t in types:
        # Polygones qui contiennent ce type
        mask = joined[joined["type_mobil"] == t]
        idx = mask.index.unique()
    
        col_name = f"has_{t}"
        network[col_name] = 0
        network.loc[idx, col_name] = 1

    # Sauvegarder
    network.to_file(network_mob_urb_path, driver="GPKG")

mob_urbain()   
    