import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
from data_utils import *
import sys
sys.path.append("../")
#Appel des données
from global_variable import *

###### NETWORK SCORE CALCULATION #######
create_folder("./output_data/network/graph/")

### GLOBAL VARIABLES ###

### FUNCTIONS ###

def ponderer_all():
    network_final = gpd.read_file(network_complet_path) 
    network_lineaire = gpd.read_file(vil_network_bounding_path, layer = "edges")
    vil_area = gpd.read_file(vil_area_path)
    vil_area = vil_area.to_crs(3946)

    fresh_value = 0
    #coef 10 (donnée en %)
    network_final["value_ombre_8h"] = abs(network_final["shad_8h"]-100)
    network_final["value_ombre_13h"] = abs(network_final["shad_13h"]-100)
    network_final["value_ombre_18h"] = abs(network_final["shad_18h"]-100)
    #coef 2
    network_final["value_assise"] = abs(network_final["assise"]*20-20)
    network_final["value_fontaine"] = abs(network_final["fontaine"]*20-20)
    #coef 7
    network_final["value_brumi"] = abs(network_final["brumisateu"]*70-70)
    network_final["value_borne_font"] = abs(network_final["borne_font"]*70-70)
    network_final["value_sanitaire"] = abs(network_final["sanitaire_"]*70-70)
    #coef 3
    network_final["value_parc"] = abs(network_final["parc_prese"]*30-30)
    #coef 8 (donnée en %)
    network_final["value_vegetation"] = abs(network_final["pct_vegeta"]-100)*0.8
    #coef 6 (valeur allant de 0 à 14 or 7*4.3=60.2)
    network_final["value_temp"] = (network_final["temp_moy"]+7)*4.3

    network_final["fresh_8h"] = (network_final["value_ombre_8h"] + network_final["value_brumi"]+ network_final["value_assise"]
    + network_final["value_borne_font"]+ network_final["value_fontaine"]+ network_final["value_parc"]+ network_final["value_sanitaire"]
    + network_final["value_vegetation"]+ network_final["value_temp"])

    network_final["fresh_13h"] = (network_final["value_ombre_13h"] + network_final["value_brumi"]+ network_final["value_assise"]
    + network_final["value_borne_font"]+ network_final["value_fontaine"]+ network_final["value_parc"]+ network_final["value_sanitaire"]
    + network_final["value_vegetation"]+ network_final["value_temp"])

    network_final["fresh_18h"] = (network_final["value_ombre_18h"] + network_final["value_brumi"]+ network_final["value_assise"]
    + network_final["value_borne_font"]+ network_final["value_fontaine"]+ network_final["value_parc"]+ network_final["value_sanitaire"]
    + network_final["value_vegetation"]+ network_final["value_temp"])

    #Création des poids qui seront utilisé par l'itinéraire
    network_final["weight08"]= network_final["length"]*network_final["fresh_8h"]/100
    network_final["weight13"]= network_final["length"]*network_final["fresh_13h"]/100
    network_final["weight18"]= network_final["length"]*network_final["fresh_18h"]/100

    
    col_freshness = ["u", "v","key", "fresh_8h", "fresh_13h", "fresh_18h","weight08","weight13","weight18"] 
    col_freshness_subset = network_final[col_freshness]

    network_lineaire_final = network_lineaire.merge(
        col_freshness_subset,
        how="left",
        left_on=["u","v","key"],
        right_on=["u","v","key"]
    )
    
    # Dissuader le passage par l'extérieur de la commune
    intersects_mask = network_lineaire_final.geometry.intersects(vil_area.union_all())
    non_intersect_mask = ~intersects_mask
    network_lineaire_final.loc[non_intersect_mask, "weight08"] += 100
    network_lineaire_final.loc[non_intersect_mask, "weight13"] += 100
    network_lineaire_final.loc[non_intersect_mask, "weight18"] += 100
    network_lineaire_final.loc[non_intersect_mask, "length"] += 100
    
    # Empêcher le passage par le périph
    highway = network_lineaire_final["highway"] == "truck"
    network_lineaire_final.loc[highway, "weight08"] += 1000
    network_lineaire_final.loc[highway, "weight13"] += 1000
    network_lineaire_final.loc[highway, "weight18"] += 1000
    network_lineaire_final.loc[highway, "length"] += 1000
    
    network_lineaire_final.to_file(network_final_path, driver="ESRI Shapefile")

ponderer_all()

