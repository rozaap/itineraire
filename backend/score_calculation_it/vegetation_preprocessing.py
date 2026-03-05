import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import os
from data_utils import *
import sys
sys.path.append("../")
#from global_variable import *

###### CREATE WORKING DIRECTORY FOR VEGETATION #######
create_folder("backend/score_calculation_it/output_data/vegetation_strat/")
vegetation_path = "backend/score_calculation_it/input_data/Vegetation_strat_Vlb/Vegetation_strat_vlb.shp"
edges_buffer_path = "backend/score_calculation_it/input_data/vil_network_bounding.gpkg"
vil_area_path = "backend/score_calculation_it/input_data/villeurbanne/villeurbanne.shp"
network_vegetation = "backend/score_calculation_it/output_data/vegetation_strat/network_Vegetation.gpkg"


###### VEGETATION STRATIFIEE PREPROCESSING ######
choice = 'OUI'#input("""
   # Souhaitez-vous mettre à jour le réseau pondéré par les parcs ? OUI ou NON
#""")
if(choice=="OUI"):
    vegetation = gpd.read_file(vegetation_path)
    network = gpd.read_file(edges_buffer_path, layer="edges_buffer")

    # Harmoniser CRS
    if network.crs != vegetation.crs:
        vegetation = vegetation.to_crs(network.crs)

    # 🔑 Ajouter un ID unique AVANT overlay
    network = network.reset_index(drop=True)
    network["net_id"] = network.index

    # Surface totale
    network["area_total"] = network.geometry.area

    # Intersection réelle
    intersection = gpd.overlay(network, vegetation, how="intersection")

    # Surface intersectée
    intersection["area_inter"] = intersection.geometry.area

    # Somme des surfaces par polygone réseau
    area_sum = (
        intersection.groupby("net_id")["area_inter"]
        .sum()
    )

    # Calcul %
    network["pct_vegetation"] = (
       network["net_id"].map(area_sum) / network["area_total"]*100
    )

    network["pct_vegetation"] = network["pct_vegetation"].fillna(0)
    
    # Sauvegarder
    network.to_file(network_vegetation, driver="GPKG")
