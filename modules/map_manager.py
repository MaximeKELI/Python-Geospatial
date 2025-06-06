import folium
from folium import plugins
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import geopandas as gpd
from shapely.geometry import Polygon, Point

class MapManager:
    def create_map(self, lat, lon, zoom_start=13):
        """Crée une carte centrée sur les coordonnées spécifiées."""
        m = folium.Map(location=[lat, lon], zoom_start=zoom_start)
        
        # Ajouter le contrôle de dessin de polygones
        draw = plugins.Draw(
            export=True,
            position='topleft',
            draw_options={
                'polyline': False,
                'polygon': True,
                'circle': False,
                'rectangle': False,
                'marker': False,
                'circlemarker': False,
            }
        )
        draw.add_to(m)
        
        return m

    def add_marker(self, map_obj, lat, lon, popup_text):
        """Ajoute un marqueur à la carte."""
        folium.Marker([lat, lon], popup=popup_text).add_to(map_obj)

    def analyze_flood_risk(self, polygon_coords, elevation_data=None, water_bodies=None):
        """
        Analyse le risque d'inondation pour une zone donnée.
        
        Args:
            polygon_coords: Liste de coordonnées [lat, lon] formant le polygone
            elevation_data: Données d'élévation (optionnel)
            water_bodies: Données des cours d'eau (optionnel)
            
        Returns:
            float: Score de risque d'inondation (0-1)
        """
        # Créer un polygone à partir des coordonnées
        polygon = Polygon([(lon, lat) for lat, lon in polygon_coords])
        
        # Calculer le centre du polygone
        center = polygon.centroid
        
        # Pour l'exemple, nous utilisons des facteurs simplifiés
        # Dans un cas réel, il faudrait utiliser des données réelles
        
        # 1. Facteur d'élévation (simulé)
        elevation_risk = np.random.random()  # Simulé pour l'exemple
        
        # 2. Facteur de proximité à l'eau (simulé)
        water_proximity_risk = np.random.random()  # Simulé pour l'exemple
        
        # 3. Facteur de pente (simulé)
        slope_risk = np.random.random()  # Simulé pour l'exemple
        
        # Combiner les facteurs avec des poids
        weights = {
            'elevation': 0.4,
            'water_proximity': 0.4,
            'slope': 0.2
        }
        
        total_risk = (
            weights['elevation'] * elevation_risk +
            weights['water_proximity'] * water_proximity_risk +
            weights['slope'] * slope_risk
        )
        
        return total_risk

    def add_risk_polygon(self, map_obj, polygon_coords, risk_score):
        """
        Ajoute un polygone coloré selon le niveau de risque à la carte.
        
        Args:
            map_obj: Objet carte Folium
            polygon_coords: Liste de coordonnées [lat, lon]
            risk_score: Score de risque (0-1)
        """
        # Déterminer la couleur en fonction du score de risque
        if risk_score < 0.3:
            color = 'green'
        elif risk_score < 0.6:
            color = 'orange'
        else:
            color = 'red'
            
        # Créer le polygone avec la couleur appropriée
        folium.Polygon(
            locations=polygon_coords,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.4,
            popup=f'Risque d\'inondation: {risk_score:.2%}'
        ).add_to(map_obj)