import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import osmnx as ox
import sys
sys.path.append("../../")
#Appel des données
from global_variable import *

"""
    The bounding_Villeurbanne file contains the bounding of Villeurbanne. It is used to define graph query limit in the
    ox.graph_from_polygon function.
"""

def globpath(path):
    return os.path.join(base_path, path)

def fetch_OSM_graph():
    """This function load an OSM graph into Villeurbanne \n
    """
    print("Reading bouding Villeurbanne")
    vil_area = gpd.read_file(vil_area_path)
    vil_area['geometry'] = vil_area.geometry.buffer(30)
    vil_area = vil_area.to_crs("4326")
    
    geometry = vil_area["geometry"].iloc[0]

    print("Fetching Graph from Villeurbannne")

    G = ox.graph_from_polygon(geometry, network_type="walk")
    #EPSG:3946 is the default projection system used by Villeurbanne.
    G = ox.project_graph(G, to_crs="EPSG:3946")

    print(f"Saving graph into {vil_network_bounding_path}")
    ox.save_graph_geopackage(G, vil_network_bounding_path)

def bufferize(input_path, output_path,layer, buffer_size):
    """Bufferize a layer according to a buffer_size and save the ouput file"""
    print("Reading edges from graph file")
    layer_gpd = gpd.read_file(input_path, layer = layer)

    print('Buffering edges')
    buffered_features = layer_gpd.geometry.apply(lambda x: x.buffer(buffer_size))

    layer_buffer = gpd.GeoDataFrame(layer_gpd.drop("geometry", axis=1), geometry=buffered_features)
    layer_buffer.crs = layer_gpd.crs

    print("Saving buffered edges")
    layer_buffer.to_file(output_path, driver="GPKG", layer="edges_buffer")

def fetch_network ():
    fetch_OSM_graph()
    #buffer de 6.25 mètre des deux côtés
    bufferize(vil_network_bounding_path, vil_network_bounding_path,"edges", 6.25)
