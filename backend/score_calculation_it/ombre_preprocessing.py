import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
from data_utils import *
import sys
import rasterio
from rasterio import features
from shapely.geometry import mapping
import numpy as np
sys.path.append("../")
#Appel des données
from global_variable import *

###### CREATE WORKING DIRECTORY FOR OMBRES ######
create_folder("backend/score_calculation_it/output_data/ombre/")

###### OMBRE PREPROCESSING ######
"""Les données proviennent du site ShadeMap à partir du 15 juillet 2025
   Sélection de trois horaires : 8h, 13h, 18h """

### SCRIPT ###
# Ce script permet de calculer le pourcentage d'ombre sur chaque différents segments de la ville

def calculate_shadows():
    network_edge = gpd.read_file(vil_network_bounding_path, layer = "edges_buffer")
    vil_area = gpd.read_file(vil_area_path)
    vil_area = vil_area.to_crs(3946)

    # Ombre à 8h
    with rasterio.open(shadows_08_path) as src: 
        raster = src.read(1)
        transform = src.transform
        nodata = src.nodata
        means = []

        # Boucle pour récupérer la part du chemin (avec le buffer) qui est à l'ombre à 8h pour chaque segment
        # Le raster d'ombre initiale à les valeurs 0 ou 255 selon si il y a de l'ombre ou du soleil
        for geom in network_edge.geometry:
            mask = features.rasterize(
                [(mapping(geom), 1)],
                out_shape=raster.shape,
                transform=transform,
                fill=0,
                dtype=np.uint8
            )
            # Creation d'un variable ou seul les pixels à l'ombre sont gardés
            touched = mask == 1
            if nodata is not None:
                values = raster[(touched) & (raster != nodata)]
            else:
                values = raster[touched]
            if len(values) > 0:
                means.append(float(values.mean()))
            else:
                means.append(np.nan)
        network_edge["shad_8h"] = means

    # Ombre à 13h   
    with rasterio.open(shadows_13_path) as src: 
        raster = src.read(1)
        transform = src.transform
        nodata = src.nodata
        means = []
        # Boucle pour récupérer la part du chemin (avec le buffer) qui est à l'ombre à 13h pour chaque segment
        # Le raster d'ombre initiale à les valeurs 0 ou 255 selon si il y a de l'ombre ou du soleil
        for geom in network_edge.geometry:
            mask = features.rasterize(
                [(mapping(geom), 1)],
                out_shape=raster.shape,
                transform=transform,
                fill=0,
                dtype=np.uint8
            )
            # Creation d'un variable ou seul les pixels à l'ombre sont gardés
            touched = mask == 1
            if nodata is not None:
                values = raster[(touched) & (raster != nodata)]
            else:
                values = raster[touched]
            if len(values) > 0:
                means.append(float(values.mean()))
            else:
                means.append(np.nan)
        network_edge["shad_13h"] = means

    # Ombre à 18h 
    with rasterio.open(shadows_18_path) as src: 
        raster = src.read(1)
        transform = src.transform
        nodata = src.nodata
        means = []
        # Boucle pour récupérer la part du chemin (avec le buffer) qui est à l'ombre à 18h pour chaque segment
        # Le raster d'ombre initiale à les valeurs 0 ou 255 selon si il y a de l'ombre ou du soleil
        for geom in network_edge.geometry:
            mask = features.rasterize(
                [(mapping(geom), 1)],
                out_shape=raster.shape,
                transform=transform,
                fill=0,
                dtype=np.uint8
            )
            # Creation d'un variable ou seul les pixels à l'ombre sont gardés
            touched = mask == 1
            if nodata is not None:
                values = raster[(touched) & (raster != nodata)]
            else:
                values = raster[touched]

            if len(values) > 0:
                means.append(float(values.mean()))
            else:
                means.append(np.nan)
        network_edge["shad_18h"] = means

    # Ajuster la valeur pour les segments hors Villeurbanne
    intersects_mask = network_edge.geometry.intersects(vil_area.union_all())
    non_intersect_mask = ~intersects_mask
    network_edge.loc[non_intersect_mask, "shad_8h"] = 0
    network_edge.loc[non_intersect_mask, "shad_13h"] = 0
    network_edge.loc[non_intersect_mask, "shad_18h"] = 0

    #Ajustement des valeurs pour avoir un pourcentage
    network_edge["shad_8h"]=network_edge["shad_8h"]/255*100
    network_edge["shad_13h"]=network_edge["shad_13h"]/255*100
    network_edge["shad_18h"]=network_edge["shad_18h"]/255*
    
    #Sortie
    network_edge.to_file(network_shadow_path, driver="GPKG", layer="network_shadow")
    
calculate_shadows()
    