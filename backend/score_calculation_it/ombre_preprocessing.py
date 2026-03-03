#%%
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
#from global_variable import *

#%%
###### CREATE WORKING DIRECTORY FOR OMBRES ######
create_folder("backend/score_calculation_it/output_data/ombre/")
shadows_08_path ="backend/score_calculation_it/input_data/ombre/8h.tif"
edges_buffer_path = "backend/score_calculation_it/input_data/vil_network_bounding.gpkg"
network_shadow_path = "backend/score_calculation_it/output_data/ombre/network_shadow.gpkg"
vil_area_path = "backend/score_calculation_it/input_data/villeurbanne/villeurbanne.shp"

##### SCRIPT #####

#%%

def calculate_shadows(): #eventuellement rajouter des paramètre pour selectionner l'heure, pour l'instant, juste 8h
    #values_shadow_08 = gpd.read_file(shadows_08_path)
    network_edge = gpd.read_file(edges_buffer_path, layer = "edges_buffer")
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

        network_edge["portion_ombre"] = means
    

    # Ajuster le valeur pour les segments hors Villeurbanne
    intersects_mask = network_edge.geometry.intersects(vil_area.union_all())
    non_intersect_mask = ~intersects_mask
    network_edge.loc[non_intersect_mask, "portion_ombre"] = 0
    network_edge["portion_ombre"]=network_edge["portion_ombre"]/255*100
    network_edge.to_file(network_shadow_path, driver="GPKG", layer="network_shadow")
    print("fini")
    

    
calculate_shadows()



#    """ """  valid_geometry = bat.make_valid()
#     bat["geometry"] = valid_geometry

#     start = time.time()
#     print("reading file ...")

#     datetimes = [datetime(2023, 6, 21, 8), datetime(2023, 6, 21, 20), timedelta(hours=5)]
#     datetimes = DatetimeLib.generate(datetimes)
#     print("start calculate shadows")
#     shadows = STHardShadow(bat, datetimes, occludersElevationFieldname='htotale',
#         altitudeOfShadowPlane=0, aggregate=True, tz=None, model='pysolar').run()

#     shadows = shadows.to_crs(3946)
#     print("save file")
#     shadows.to_file(shadows_path, driver="GPKG", layer="shadow")

# # end = time.time()

# # duration = (end-start)/60
# # print("duration : ", duration) # around 4 hours

#     ###### SPLIT SHADOWS INTO SCHEDULE ######
#     shadows = gpd.read_file(shadows_path)

#     shadows_08 = shadows[shadows["datetime"] == "2023-06-21 08:00:00+00:00"]
#     shadows_13 = shadows[shadows["datetime"] == "2023-06-21 13:00:00+00:00"]
#     shadows_18 = shadows[shadows["datetime"] == "2023-06-21 18:00:00+00:00"]

#     shadows_08.to_file(shadows_08_path)
#     shadows_13.to_file(shadows_13_path)
#     shadows_18.to_file(shadows_18_path)

#     ##### CLIP SHADOWS WITH EDGES #####
#     print("##### CLIP SHADOWS WITH EDGES #####")
#     print("8h")
#     clip_data(edges_buffer_path, shadows_08_path, shadows_08_clipped_path, 4, "ombres")
#     print("13h")
#     clip_data(edges_buffer_path, shadows_13_path, shadows_13_clipped_path, 4, "ombres")
#     print("18h")
#     clip_data(edges_buffer_path, shadows_18_path, shadows_18_clipped_path, 4, "ombres")

#     #### EXPLODE SHADOWS INTO SEVERAL POLYGONS #####
#     print("##### EXPLODE SHADOWS INTO SEVERAL POLYGONS #####")
#     print("8h")
#     explode_polygon(shadows_08_clipped_path, shadows_08_explode_path)
#     print("13h")
#     explode_polygon(shadows_13_clipped_path, shadows_13_explode_path)
#     print("18h")
#     explode_polygon(shadows_18_clipped_path, shadows_18_explode_path)

#     #### CALCULATE INTERSECTION #####
#     print("##### CALCULATE INTERSECTION #####")
#     print("8h")
#     overlay_intersect(edges_buffer_path, shadows_08_explode_path, shadows_08_intersect_path)
#     print("13h")
#     overlay_intersect(edges_buffer_path, shadows_13_explode_path, shadows_13_intersect_path)
#     print("18h")
#     overlay_intersect(edges_buffer_path, shadows_18_explode_path, shadows_18_intersect_path)


#     #### CALCULATE SHADOWS PROPORTION ON EDGES ######
#     print("###### CALCULATE SHADOWS PROPORTION ON EDGES ######")

#     print("Calculate shadows proportion")
#     print("8h")
#     calculate_area_proportion(edges_buffer_path, shadows_08_intersect_path, "ombres", edges_buffer_ombres_08_prop_path, "edges")
#     print("13h")
#     calculate_area_proportion(edges_buffer_path, shadows_13_intersect_path, "ombres", edges_buffer_ombres_13_prop_path, "edges")
#     print("13h")
#     calculate_area_proportion(edges_buffer_path, shadows_18_intersect_path, "ombres", edges_buffer_ombres_18_prop_path, "edges")

# #%%
#     ombre_13 = gpd.read_file(edges_buffer_ombres_13_prop_path)
#     ombre_13 = ombre_13.rename(columns={"ombres_prop": "ombres_13_prop"})
#     ombre_13.to_file(edges_buffer_ombres_13_prop_path, driver="GPKG", layer="edges")

#     ombre_18 = gpd.read_file(edges_buffer_ombres_18_prop_path)
#     ombre_18 = ombre_18.rename(columns={"ombres_prop": "ombres_18_prop"})
#     ombre_18.to_file(edges_buffer_ombres_18_prop_path, driver="GPKG", layer="edges")
#  # %% 