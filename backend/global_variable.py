import os
### GLOBAL VARIABLES OF THE PROJECT ###

base_path = os.path.dirname(os.path.abspath(__file__))

def globpath(path):
    return os.path.join(base_path, path)

### EMPRISE DE VILLEURBANNE PATH ###
bounding_Villeurbanne_path = globpath("score_calculation_it/input_data/bounding_vil.gpkg")

### NETWORK PATH ###
vil_network_bounding_path = globpath("score_calculation_it/input_data/vil_network_bounding.gpkg")
vil_area_path = globpath("score_calculation_it/input_data/villeurbanne/villeurbanne.shp")

### GRAPH PATH ###
network_complet_path = globpath("score_calculation_it/output_data/network/network_complet.shp")
network_final_path = globpath("score_calculation_it/output_data/network/network_final.shp")

### DATA PATH ### 

#OMBRES : jour choisi : 15 juillet 2025
shadows_08_path = globpath("score_calculation_it/input_data/ombre/8h.tif")
shadows_13_path = globpath("score_calculation_it/input_data/ombre/13h.tif")
shadows_18_path = globpath("score_calculation_it/input_data/ombre/18h.tif")
network_shadow_path = globpath("score_calculation_it/output_data/ombre/network_shadow.gpkg")

#SANITAIRES
sanitaire_path = globpath("score_calculation_it/input_data/sanitaires/Sanitaires.shp")
network_sanitaire_path = globpath("score_calculation_it/output_data/Sanitaire/network_Sanitaire.gpkg")

#MOBILIER URBAIN
mob_urbain_path = globpath("score_calculation_it/input_data/Mobilier_urbain/Mobilierurbain.shp")
network_mob_urb_path = globpath("score_calculation_it/output_data/mobilier_urbain/network_mobilier_urbain.gpkg")

#VEGETATION STRATIFIE
vegetation_path = globpath("score_calculation_it/input_data/Vegetation_strat_Vlb/Vegetation_strat_vlb.shp")
network_vegetation_path = globpath("score_calculation_it/output_data/vegetation_strat/network_Vegetation.gpkg")

#TEMPERATURE AU SOL
temp_path = globpath("score_calculation_it/input_data/Temperature/villeurbanne25_LST2024_DistTempMean_3946.tiff")
network_temp_path = globpath("score_calculation_it/output_data/temp/network_temp.gpkg")

#PARC
espacevert_path = globpath("score_calculation_it/input_data/EV_EspaceVert/EV_EspaceVert.shp")
network_espacevert_path = globpath("score_calculation_it/output_data/EspaceVert/network_EspaceVert.gpkg")


