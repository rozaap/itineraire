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
from global_variable import *

###### CREATE WORKING DIRECTORY FOR OMBRES ######
create_folder("backend/score_calculation_it/output_data/ombre/")
# shadows_08_path ="backend/score_calculation_it/input_data/ombre/8h.tif"
# shadows_13_path ="backend/score_calculation_it/input_data/ombre/13h.tif"
# shadows_18_path ="backend/score_calculation_it/input_data/ombre/18h.tif"
# edges_buffer_path = "backend/score_calculation_it/input_data/vil_network_bounding_buffer.gpkg"
# network_shadow_path = "backend/score_calculation_it/output_data/ombre/network_shadow.gpkg"
# vil_area_path = "backend/score_calculation_it/input_data/villeurbanne/villeurbanne.shp"

##### SCRIPT #####

def calculate_shadows():
    network_edge = gpd.read_file(vil_network_bounding_path, layer = "edges_buffer")
    vil_area = gpd.read_file(vil_area_path)
    vil_area = vil_area.to_crs(3946)

    with rasterio.open(shadows_08_path) as src: 
        raster = src.read(1)
        transform = src.transform
        nodata = src.nodata
        raster_crs = src.crs
        means = []
        for geom in network_edge.geometry:

            # Rasteriser la ligne
            mask = features.rasterize(
                [(mapping(geom), 1)],
                out_shape=raster.shape,
                transform=transform,
                fill=0,
                dtype=np.uint8
            )
            
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

    with rasterio.open(shadows_13_path) as src: 
        raster = src.read(1)
        transform = src.transform
        nodata = src.nodata
        raster_crs = src.crs
        means = []
        for geom in network_edge.geometry:

            # Rasteriser la ligne
            mask = features.rasterize(
                [(mapping(geom), 1)],
                out_shape=raster.shape,
                transform=transform,
                fill=0,
                dtype=np.uint8
            )
            
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

    with rasterio.open(shadows_18_path) as src: 
        raster = src.read(1)
        transform = src.transform
        nodata = src.nodata
        raster_crs = src.crs
        means = []
        for geom in network_edge.geometry:

            # Rasteriser la ligne
            mask = features.rasterize(
                [(mapping(geom), 1)],
                out_shape=raster.shape,
                transform=transform,
                fill=0,
                dtype=np.uint8
            )
            
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
    network_edge["shad_8h"]=network_edge["shad_8h"]/255*100
    network_edge["shad_13h"]=network_edge["shad_13h"]/255*100
    network_edge["shad_18h"]=network_edge["shad_18h"]/255*100
    network_edge.to_file(network_shadow_path, driver="GPKG", layer="network_shadow")
    
calculate_shadows()
    