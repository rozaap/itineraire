import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import osmnx as ox
import sys
sys.path.append("../../")
from global_variable import *

"""
    The bounding_Villeurbanne file contains the bounding of Villeurbanne. It is used to define graph query limit in the
    ox.graph_from_polygon function.
"""

def globpath(path):
    return os.path.join(base_path, path)


#network_filters = "[\"highway\"][\"area\"!~\"yes\"][\"highway\"!~\"abandoned|bus_guideway|construction|cycleway|motorway|trunk|planned|platform|proposed|raceway|motorway_link|trunk_link|escape|busway\"][\"foot\"!~\"no\"][\"service\"!~\"private\"][\"sidewalk\"!~\"no\"]"

def fetch_OSM_graph():
    """This function load an OSM graph into the Metropole of Lyon \n
    """
    print("Reading bouding Villeurbanne")
    bounding_Vil = gpd.read_file(bounding_Villeurbanne_path)
    bounding_Vil = bounding_Vil.to_crs("4326")
    
    geometry = bounding_Vil["geometry"].iloc[0]

    print("Fetching Graph from Lyon Metropole")
    #G = ox.graph_from_polygon(geometry, custom_filter=network_filters)
    G = ox.graph_from_polygon(geometry, network_type="walk")
    print(bounding_Vil)
    #EPSG:3946 is the default projection system used by Villeurbanne.
    G = ox.project_graph(G, to_crs="EPSG:3946")

    print(f"Saving graph into {Vil_network_bounding_path}")
    ox.save_graph_geopackage(G, Vil_network_bounding_path)

def bufferize(input_path, output_path, layer, buffer_size):
    """Bufferize a layer according to a buffer_size and save the ouput file"""
    print("Reading edges from graph file")
    layer_gpd = gpd.read_file(input_path, layer=layer)

    layer_gpd = layer_gpd.to_crs(3946)

    print('Buffering edges')
    buffered_features = layer_gpd.geometry.apply(lambda x: x.buffer(buffer_size))

    layer_buffer = gpd.GeoDataFrame(layer_gpd.drop("geometry", axis=1), geometry=buffered_features)
    layer_buffer.crs = layer_gpd.crs

    print("Saving buffered edges")
    layer_buffer.to_file(output_path, driver="GPKG", layer=layer)


choice = input("Voulez vous télécharger le réseau (NETWORK) et le bufferizer (BUFFER) ou faire les deux (ALL)? \n Veuillez saisir une des 3 possibilitées : NETWORk, BUFFER, ALL : \n")

if(choice == "ALL"):
    fetch_OSM_graph()
    bufferize(bounding_Villeurbanne_path, edges_buffer_path, "main.edges", 6.25)
elif(choice== "NETWORK"):
    fetch_OSM_graph()
elif(choice == "BUFFER"):
    bufferize(bounding_Villeurbanne_path, edges_buffer_path, "main.edges", 6.25)
else:
    print("Veuillez saisir un choix valide")
