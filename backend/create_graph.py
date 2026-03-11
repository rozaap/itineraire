import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import networkx as nx
import sys

# Ajouter le dossier contenant fetch_network.py au PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "score_calculation_it", "input_data")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "score_calculation_it")))
# Maintenant Python peut trouver fetch_network
#from fetch_network import fetch_network
from ombre_preprocessing import calculate_shadows
from mobilier_urbain_preprocessing import mob_urbain
from sanitaire_preprocessing import sanitaire
from vegetation_preprocessing import vegetation
from temperature_preprocessing import calculate_temperature
from parcs_jardins_preprocessing import parc
from network_link_coolspot import link_data_together
from score_calculation import ponderer_all


def create_graph():
    choice_complet = "OUI"
    # choice_complet = input("""
    #     Souhaitez-vous tout mettre à jour ? (faire touner l'ensemble du code) OUI ou NON 
    # """)
    if (choice_complet == "OUI"):
        # COMMENTER LES DONNEES NON MODIFIE
        #fetch_network()
        calculate_shadows()
        mob_urbain()
        sanitaire()
        vegetation()
        calculate_temperature()
        parc()
        link_data_together()
        ponderer_all()
    else : 
        choice = input("""
            Souhaitez-vous mettre à jour le graph (sans les pondérations)? OUI ou NON
        """)
        if (choice=='OUI'):
            fetch_network()

        choice = input("""
            Souhaitez-vous mettre à jour les données d'ombres ? OUI ou NON
        """)
        if (choice=='OUI'):
            calculate_shadows()

        choice = input("""
             Souhaitez-vous mettre à jour les données de mobiliers urbains? OUI ou NON
        """)
        if (choice=='OUI'):
            mob_urbain()

        choice = input("""
            Souhaitez-vous mettre à jour les données de sanitaire ? OUI ou NON
        """)
        if (choice=='OUI'):
            sanitaire()

        choice = input("""
            Souhaitez-vous mettre à jour les données de végétation ? OUI ou NON
        """)
        if (choice=='OUI'):
            vegetation()

        choice = input("""
            Souhaitez-vous mettre à jour les données de température ? OUI ou NON
        """)
        if (choice=='OUI'):
            calculate_temperature()

        choice = input("""
            Souhaitez-vous mettre à jour les données de parc ? OUI ou NON
        """)
        if (choice=='OUI'):
            parc()
        link_data_together()
        ponderer_all()


create_graph()

    


