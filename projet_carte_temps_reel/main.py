import sys
import os

# Ajouter le dossier racine au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.map_manager import MapManager
from modules.data_handler import DataHandler
import folium
import pandas as pd
from streamlit_folium import folium_static
import streamlit as st

# Configuration de la page Streamlit
st.set_page_config(page_title="Carte en temps réel", layout="wide")
st.title("Visualisation de carte en temps réel")

# Initialisation des modules
map_manager = MapManager()
data_handler = DataHandler()

# Chemin absolu vers gps_data.json
data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "gps_data.json")

# Charger des données GPS (exemple)
data = data_handler.load_data(data_path)

# Créer une carte centrée sur la première position
initial_lat, initial_lon = data.iloc[0]["latitude"], data.iloc[0]["longitude"]
m = map_manager.create_map(initial_lat, initial_lon)

# Ajouter des marqueurs pour chaque point GPS
for index, row in data.iterrows():
    map_manager.add_marker(m, row["latitude"], row["longitude"], row["description"])

# Afficher la carte dans Streamlit
folium_static(m)

# Interface utilisateur pour ajouter un marqueur
with st.sidebar:
    st.header("Ajouter un marqueur")
    lat = st.number_input("Latitude", value=initial_lat)
    lon = st.number_input("Longitude", value=initial_lon)
    desc = st.text_input("Description")
    if st.button("Ajouter"):
        map_manager.add_marker(m, lat, lon, desc)
        st.success("Marqueur ajouté !")
        folium_static(m)