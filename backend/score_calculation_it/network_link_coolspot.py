import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import os
from data_utils import *
import sys
sys.path.append("../")
from global_variable import *

###### CREATE WORKING DIRECTORY FOR VEGETATION #######
create_folder("backend/score_calculation_it/output_data/network/")

# network_mob_urb_path = "backend/score_calculation_it/output_data/mobilier_urbain/network_mobilier_urbain.gpkg"
# network_espacevert_path = "backend/score_calculation_it/output_data/EspaceVert/network_EspaceVert.gpkg"
# network_shadow_path = "backend/score_calculation_it/output_data/ombre/network_shadow.gpkg"
# network_sanitaire_path = "backend/score_calculation_it/output_data/Sanitaire/network_Sanitaire.gpkg"
# network_vegetation_path = "backend/score_calculation_it/output_data/vegetation_strat/network_Vegetation.gpkg"
# network_temp_path = "backend/score_calculation_it/output_data/temp/network_temp.gpkg"

# network_final_path = "backend/score_calculation_it/output_data/network/network_complet.shp"

###### VEGETATION STRATIFIEE PREPROCESSING ######
def link_data_together():
    network_shadow = gpd.read_file(network_shadow_path)
    network_mob_urb = gpd.read_file(network_mob_urb_path)
    network_espacevert = gpd.read_file(network_espacevert_path)
    network_sanitaire = gpd.read_file(network_sanitaire_path)
    network_vegetation = gpd.read_file(network_vegetation_path)
    network_temp = gpd.read_file(network_temp_path)

    network_final = network_shadow

    #Ajout donnée mobilier urbain
    col_mob_urb = ["u", "v", "has_Brumisateur", "has_Assise", "has_Borne fontaine", "has_Fontaine"] 
    col_mob_urb_subset = network_mob_urb[col_mob_urb]
    col_mob_urb_subset.rename(
        columns={
            "has_Brumisateur": "brumisateur",
            "has_Assise": "assise",
            "has_Borne fontaine": "borne_fontaine",
            "has_Fontaine": "fontaine"
        },
        inplace=True
    )

    network_final = network_final.merge(
        col_mob_urb_subset,
        how="left",
        left_on=["u","v"],
        right_on=["u","v"]
    )

    #Ajout donnée parc
    col_mob_EV = ["u", "v", "parc_present"] 
    col_mob_EV_subset = network_espacevert[col_mob_EV]

    network_final = network_final.merge(
        col_mob_EV_subset,
        how="left",
        left_on=["u","v"],
        right_on=["u","v"]
    )

    #Ajout donnée sanitaire
    col_mob_sanitaire = ["u", "v", "sanitaire_present"] 
    col_mob_sanitaire_subset = network_sanitaire[col_mob_sanitaire]

    network_final = network_final.merge(
        col_mob_sanitaire_subset,
        how="left",
        left_on=["u","v"],
        right_on=["u","v"]
    )


    #Ajout donnée végétation
    col_mob_vegetation = ["u", "v", "pct_vegetation"] 
    col_mob_vegetation_subset = network_vegetation[col_mob_vegetation]

    network_final = network_final.merge(
        col_mob_vegetation_subset,
        how="left",
        left_on=["u","v"],
        right_on=["u","v"]
    )


    #Ajout donnée température
    col_mob_temp = ["u", "v", "temp_moy"] 
    col_mob_temp_subset = network_temp[col_mob_temp]

    network_final = network_final.merge(
        col_mob_temp_subset,
        how="left",
        left_on=["u","v"],
        right_on=["u","v"]
    )

    network_final.to_file(network_complet_path, driver="ESRI Shapefile")


link_data_together()