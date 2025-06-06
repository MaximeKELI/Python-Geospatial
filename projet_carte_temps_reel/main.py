import sys
import os
import json
import requests
from datetime import datetime

# Ajouter le dossier racine au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.map_manager import MapManager
from modules.data_handler import DataHandler
import folium
import pandas as pd
from streamlit_folium import folium_static
import streamlit as st

# Configuration de la page Streamlit
st.set_page_config(page_title="Analyse de Risque d'Inondation", layout="wide")
st.title("Analyse de Risque d'Inondation en Temps Réel")

# Configuration de l'API
API_URL = "http://localhost:8000"

# Initialisation des modules
map_manager = MapManager()
data_handler = DataHandler()

# Créer une carte centrée sur Paris
initial_lat, initial_lon = 48.8566, 2.3522
m = map_manager.create_map(initial_lat, initial_lon)

# Afficher la carte dans Streamlit
st.subheader("Carte Interactive")
st.write("Dessinez un polygone sur la carte pour analyser le risque d'inondation")
folium_static(m)

# Récupérer les données du polygone dessiné
st.subheader("Analyse de Risque")
st.write("Une fois que vous avez dessiné un polygone sur la carte, cliquez sur le bouton ci-dessous pour analyser le risque d'inondation")

if st.button("Analyser le Risque d'Inondation"):
    try:
        # Dans un cas réel, nous récupérerions les coordonnées du polygone dessiné
        # Pour l'exemple, nous utilisons un polygone fictif
        sample_polygon = {
            "coordinates": [
                {"lat": 48.8566, "lon": 2.3522},
                {"lat": 48.8576, "lon": 2.3522},
                {"lat": 48.8576, "lon": 2.3532},
                {"lat": 48.8566, "lon": 2.3532},
                {"lat": 48.8566, "lon": 2.3522}
            ]
        }
        
        # Appeler l'API pour analyser le risque
        response = requests.post(f"{API_URL}/analyze-risk", json=sample_polygon)
        if response.status_code == 200:
            result = response.json()
            
            # Afficher le résultat principal
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Score de risque d'inondation",
                    f"{result['risk_score']:.1%}",
                    f"Niveau: {result['risk_level']}"
                )
                st.metric(
                    "Confiance de l'analyse",
                    f"{result['confidence']:.1%}"
                )
            
            # Afficher les facteurs de risque
            with col2:
                st.subheader("Facteurs de Risque Actuels")
                factors = result['factors']
                st.write(f"Élévation : {factors['elevation']:.1f} m")
                st.write(f"Pente : {factors['slope']:.1f}°")
                st.write(f"Précipitations : {factors['precipitation']:.1f} mm")
                st.write(f"Niveau d'eau : {factors['water_level']:.1f} m")
            
            # Afficher les données historiques
            st.subheader("Données Historiques")
            historical = result['historical_data']
            col3, col4, col5 = st.columns(3)
            
            with col3:
                st.metric(
                    "Nombre total d'inondations",
                    historical['total_floods']
                )
                st.metric(
                    "Fréquence annuelle",
                    f"{historical['flood_frequency']:.1f}/an"
                )
            
            with col4:
                st.metric(
                    "Sévérité moyenne",
                    historical['average_severity']
                )
                if historical['last_flood']:
                    last_flood_date = datetime.fromisoformat(
                        historical['last_flood']['date']
                    )
                    st.metric(
                        "Dernière inondation",
                        last_flood_date.strftime("%d/%m/%Y")
                    )
            
            with col5:
                st.write("Distribution des sévérités")
                severity_dist = historical['severity_distribution']
                st.write(f"Faible : {severity_dist['low']}")
                st.write(f"Moyenne : {severity_dist['medium']}")
                st.write(f"Élevée : {severity_dist['high']}")
            
            # Ajouter le polygone coloré à la carte
            polygon_coords = [[coord['lat'], coord['lon']] for coord in sample_polygon['coordinates']]
            map_manager.add_risk_polygon(m, polygon_coords, result['risk_score'])
            
            # Réafficher la carte mise à jour
            folium_static(m)
        else:
            st.error("Erreur lors de l'analyse du risque d'inondation")
    except Exception as e:
        st.error(f"Erreur : {str(e)}")

# Ajouter des informations sur les facteurs de risque
st.sidebar.header("Facteurs de Risque")
st.sidebar.write("""
Le risque d'inondation est calculé en fonction de plusieurs facteurs :
- Élévation du terrain (25%)
- Pente du terrain (15%)
- Précipitations (25%)
- Niveau d'eau (15%)
- Données historiques (20%)
""")

# Ajouter des informations sur les couleurs
st.sidebar.header("Légende")
st.sidebar.write("""
- 🟢 Vert : Risque faible (< 30%)
- 🟠 Orange : Risque moyen (30-60%)
- 🔴 Rouge : Risque élevé (> 60%)
""")

# Ajouter des informations sur la confiance
st.sidebar.header("Niveau de Confiance")
st.sidebar.write("""
Le niveau de confiance est calculé en fonction de :
- Qualité des données météo
- Qualité des données hydrologiques
- Qualité des données historiques
""")