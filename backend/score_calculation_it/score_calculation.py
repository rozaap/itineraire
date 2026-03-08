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

    fresh_value = 0
    for index, row in network_final.iterrows():
        #Pondération arbitraire
        value_ombre_8h = abs(row["shad_8h"]*8-800)
        value_ombre_13h = abs(row["shad_13h"]*8-800)
        value_ombre_18h = abs(row["shad_18h"]*8-800)
        value_brumi = abs(row["brumisateu"]*20-20)
        value_assise = abs(row["assise"]*2-2)
        value_borne_font = abs(row["borne_font"]*10-10)
        value_fontaine = abs(row["fontaine"]*10-10)
        value_parc = abs(row["parc_prese"]*30-30)
        value_sanitaire = abs(row["sanitaire_"]*10-10)
        value_vegetation = abs(row["pct_vegeta"]*8-800)
        value_temp = (row["temp_moy"]+7)*5

        #Code pour des calculs plus complexe éventuels
        # value_ombre = ponderer_ombre(index)
        # value_brumi = ponderer_brumi(index)
        # value_assise = ponderer_assise(index)
        # value_borne_font = ponderer_borne_font(index)
        # value_fontaine = ponderer_fontaine(index)
        # value_parc = ponderer_parc_present(index)
        # value_sanitaire = ponderer_sanitaire_present(index)
        # value_vegetation = ponderer_vegetation_present(index)
        # value_temp = ponderer_temp_present(index)

        fresh_8h = value_ombre_8h+value_brumi+value_assise+value_borne_font+value_fontaine+value_parc+value_sanitaire+value_vegetation+ value_temp
        fresh_13h = value_ombre_13h+value_brumi+value_assise+value_borne_font+value_fontaine+value_parc+value_sanitaire+value_vegetation+ value_temp
        fresh_18h = value_ombre_18h+value_brumi+value_assise+value_borne_font+value_fontaine+value_parc+value_sanitaire+value_vegetation+ value_temp
        network_final.loc[index, "fresh_8h"] = fresh_8h
        network_final.loc[index, "fresh_13h"] = fresh_13h
        network_final.loc[index, "fresh_18h"] = fresh_18h
        #Création des poids qui seront utilisé par l'itinéraire
        network_final["weight08"]= network_final["length"]*network_final["fresh_8h"]
        network_final["weight13"]= network_final["length"]*network_final["fresh_13h"]
        network_final["weight18"]= network_final["length"]*network_final["fresh_18h"]
    
    col_freshness = ["u", "v", "fresh_8h", "fresh_13h", "fresh_18h","weight08","weight13","weight18"] 
    col_freshness_subset = network_final[col_freshness]

    network_lineaire_final = network_lineaire.merge(
        col_freshness_subset,
        how="left",
        left_on=["u","v"],
        right_on=["u","v"]
    )
    
    

    network_lineaire_final.to_file(network_final_path, driver="ESRI Shapefile")

ponderer_all()



# def ponderer_ombre(index):
#     return (abs(network_final.loc[index, "portion_om"]*8-800))

# def ponderer_brumi(index):
#     return (abs(network_final.loc[index, "brumisateu"]*20-20))

# def ponderer_assise(index):
#     return (abs(network_final.loc[index, "assise"]*2-2))

# def ponderer_borne_font(index):
#     return (abs(network_final.loc[index, "borne_font"]*10-10))

# def ponderer_fontaine(index):
#     return (abs(network_final.loc[index, "fontaine"]*10-10))

# def ponderer_parc_present(index):
#     return (abs(network_final.loc[index, "parc_prese"]*30-30))

# def ponderer_sanitaire_present(index):
#     return (abs(network_final.loc[index, "sanitaire_"]*10-10))

# def ponderer_vegetation_present(index):
#     return (abs(network_final.loc[index, "pct_vegeta"]*8-800))

# def ponderer_temp_present(index):
#     return ((network_final.loc[index, "temp_moy"]+7)*5)

