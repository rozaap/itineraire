import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import numpy as np
import os
from data_utils import * #pour la fonction create_folder
import sys
from shapely.geometry import mapping
import rasterio
from rasterstats import zonal_stats
sys.path.append("../")
#Appel des données
from global_variable import *

###### CREATE WORKING DIRECTORY FOR TEMPERATURE ######
create_folder("backend/score_calculation_it/output_data/temp/")

###### TEMPERATURE PREPROCESSING ######
"""Les données proviennent de la mairie de Villeurbanne """
"""Explication de l'indice utilisé : https://greencity.terranis.fr/geonetwork/srv/fre/catalog.search#/metadata/1b07841e-19df-4449-81b6-9334c1d3526d"""

### SCRIPT ###
# Ce script permet de calculer la température moyenne sur chaque différents segments de la ville

###### TEMPERATURE PREPROCESSING ######

### FUNCTION ###
def calculate_temperature():
    network_edge = gpd.read_file(vil_network_bounding_path, layer = "edges_buffer")
    vil_area = gpd.read_file(vil_area_path)
    vil_area = vil_area.to_crs(3946)

    raster_crs = 3946
    network_edge = network_edge.to_crs(raster_crs)
    vil_area = vil_area.to_crs(raster_crs)

    # Calcul de la moyenne
    stats = zonal_stats(
        network_edge,
        temp_path,
        stats="mean",
        nodata=40,
       all_touched=True
    )
    network_edge["temp_moy"] = [s["mean"] for s in stats]

    # Remplacer uniquement les polygones hors Villeurbanne par 40 (pour avoir une valeur haute et ainsi éviter d'avoir un itinéraire hors zone d'étude)
    intersects_mask = network_edge.geometry.intersects(vil_area.union_all())
    non_intersect_mask = ~intersects_mask
    network_edge.loc[non_intersect_mask, "temp_moy"] = 40

    # Remplacer les valeurs None restantes par 40 (hors de Villeurbanne)
    mask = network_edge['temp_moy'].isna()
    network_edge.loc[mask, 'temp_moy'] = 40

    network_edge.to_file(network_temp_path, driver="GPKG", layer="network_shadow")
    

calculate_temperature()