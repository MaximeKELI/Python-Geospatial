import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from shapely.geometry import Polygon
import time

# Configuration de la page avec des paramètres optimisés
st.set_page_config(
    page_title="Analyse de Risque d'Inondation",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre de l'application
st.title("🌊 Analyse de Risque d'Inondation en Temps Réel")

# URL de l'API avec timeout
API_URL = "http://127.0.0.1:8000"
TIMEOUT = 30  # secondes

# Fonction pour créer la carte
def create_map():
    # Créer une carte centrée sur la France
    m = folium.Map(
        location=[46.603354, 1.888334],
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    # Ajouter le contrôle de dessin avec des options optimisées
    draw_control = folium.plugins.Draw(
        export=True,
        position='topleft',
        draw_options={
            'polyline': False,
            'rectangle': False,
            'circle': False,
            'circlemarker': False,
            'marker': False,
            'polygon': True
        }
    )
    m.add_child(draw_control)
    
    return m

# Fonction pour analyser le risque avec gestion des timeouts
def analyze_risk(coordinates):
    try:
        # Préparer les données pour l'API
        data = {
            "coordinates": [
                {"lat": coord[0], "lon": coord[1]}
                for coord in coordinates
            ]
        }
        
        # Appeler l'API avec timeout
        response = requests.post(
            f"{API_URL}/analyze-risk",
            json=data,
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API: {response.text}")
            return None
    except requests.Timeout:
        st.error("Le serveur met trop de temps à répondre. "
                 "Veuillez réessayer.")
        return None
    except Exception as e:
        st.error(f"Erreur lors de l'analyse: {str(e)}")
        return None

# Fonction pour obtenir les données météo avec timeout
def get_weather(lat, lon):
    try:
        response = requests.get(
            f"{API_URL}/weather/{lat}/{lon}",
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.warning("Données météo non disponibles")
            return None
    except requests.Timeout:
        st.warning("Données météo non disponibles")
        return None
    except Exception as e:
        st.warning("Données météo non disponibles")
        return None

# Fonction pour obtenir le niveau d'eau avec timeout
def get_water_level(lat, lon):
    try:
        response = requests.get(
            f"{API_URL}/water-level/{lat}/{lon}",
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.warning("Données de niveau d'eau non disponibles")
            return None
    except requests.Timeout:
        st.warning("Données de niveau d'eau non disponibles")
        return None
    except Exception as e:
        st.warning("Données de niveau d'eau non disponibles")
        return None

# Interface principale
def main():
    # Créer deux colonnes
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Carte Interactive")
        # Afficher la carte
        m = create_map()
        drawn_data = st_folium(m, width=800, height=600)
        
        # Bouton pour analyser
        if st.button("Analyser la zone sélectionnée"):
            if drawn_data and 'all_drawings' in drawn_data and drawn_data['all_drawings']:
                # Récupérer les coordonnées du dernier dessin
                last_drawing = drawn_data['all_drawings'][-1]
                if 'geometry' in last_drawing:
                    coordinates = last_drawing['geometry']['coordinates'][0]
                    
                    # Afficher un spinner pendant l'analyse
                    with st.spinner('Analyse en cours...'):
                        # Analyser le risque
                        result = analyze_risk(coordinates)
                        if result:
                            st.session_state['analysis_result'] = result
                            
                            # Obtenir les données météo et niveau d'eau
                            center = Polygon(coordinates).centroid
                            weather = get_weather(center.y, center.x)
                            water = get_water_level(center.y, center.x)
                            
                            st.session_state['weather_data'] = weather
                            st.session_state['water_data'] = water
            else:
                st.warning("Veuillez d'abord dessiner une zone sur la carte.")
    
    with col2:
        st.subheader("Résultats de l'analyse")
        
        # Afficher les résultats si disponibles
        if 'analysis_result' in st.session_state:
            result = st.session_state['analysis_result']
            
            # Score de risque
            st.metric(
                "Score de risque",
                f"{result['risk_score']:.2%}",
                delta=None
            )
            
            # Niveau de risque
            risk_level = result['risk_level']
            risk_color = {
                'faible': 'green',
                'moyen': 'orange',
                'élevé': 'red'
            }.get(risk_level, 'gray')
            
            st.markdown(
                f"<h3 style='color: {risk_color};'>"
                f"Niveau de risque: {risk_level}</h3>",
                unsafe_allow_html=True
            )
            
            # Facteurs de risque
            st.subheader("Facteurs de risque")
            for factor, value in result['factors'].items():
                st.write(f"- {factor}: {value}")
            
            # Données météo
            if 'weather_data' in st.session_state and st.session_state['weather_data']:
                weather = st.session_state['weather_data']
                st.subheader("Données météorologiques")
                st.write(f"Température: {weather['temperature']}°C")
                st.write(f"Précipitations: {weather['precipitation']} mm")
                st.write(f"Humidité: {weather['humidity']}%")
                st.write(f"Vitesse du vent: {weather['wind_speed']} m/s")
            
            # Niveau d'eau
            if 'water_data' in st.session_state and st.session_state['water_data']:
                water = st.session_state['water_data']
                st.subheader("Niveau d'eau")
                st.write(f"Niveau: {water['level']} m")
                st.write(f"Tendance: {water['trend']}")
                st.write(f"Source: {water['source']}")


if __name__ == "__main__":
    main() 