from typing import List, Dict, Any
from datetime import datetime
import numpy as np
from shapely.geometry import Polygon as ShapelyPolygon
from shapely.geometry import Point
import geopandas as gpd
from sklearn.ensemble import RandomForestClassifier
from models import Polygon, FloodRiskAnalysis, WeatherData, WaterLevelData
import elevation
import rasterio
from rasterio.warp import transform
import requests
from geopy.distance import geodesic
import os
from dotenv import load_dotenv
from historical_data import HistoricalDataService

load_dotenv()

class ElevationService:
    def __init__(self):
        self.elevation_data = None

    def get_elevation(self, lat: float, lon: float) -> float:
        """Récupère l'élévation pour un point donné."""
        try:
            # Simuler l'élévation pour l'exemple
            return np.random.uniform(0, 100)
        except Exception as e:
            print(f"Erreur lors de la récupération de l'élévation: {e}")
            return np.random.uniform(0, 100)  # Valeur par défaut simulée

    def get_slope(self, lat: float, lon: float) -> float:
        """Calcule la pente pour un point donné."""
        # Dans un cas réel, nous utiliserions des données DEM pour calculer la pente
        # Pour l'exemple, nous retournons une valeur aléatoire
        return np.random.uniform(0, 45)

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5"

    def get_weather_data(self, lat: float, lon: float):
        """Récupère les données météorologiques pour un point donné."""
        try:
            if not self.api_key:
                # Retourner des données simulées si pas de clé API
                return {
                    "temperature": np.random.uniform(10, 30),
                    "precipitation": np.random.uniform(0, 10),
                    "humidity": np.random.uniform(30, 90),
                    "wind_speed": np.random.uniform(0, 10),
                    "timestamp": datetime.now()
                }

            url = f"{self.base_url}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            response = requests.get(url, params=params)
            data = response.json()
            
            return {
                "temperature": data["main"]["temp"],
                "precipitation": data.get("rain", {}).get("1h", 0),
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "timestamp": datetime.fromtimestamp(data["dt"])
            }
        except Exception as e:
            print(f"Erreur lors de la récupération des données météo: {e}")
            # Retourner des données simulées en cas d'erreur
            return {
                "temperature": np.random.uniform(10, 30),
                "precipitation": np.random.uniform(0, 10),
                "humidity": np.random.uniform(30, 90),
                "wind_speed": np.random.uniform(0, 10),
                "timestamp": datetime.now()
            }

class WaterService:
    def __init__(self):
        self.api_key = os.getenv("WATER_API_KEY")
        self.base_url = "https://api.waterdata.com"  # URL fictive

    def get_water_level(self, lat: float, lon: float):
        """Récupère le niveau d'eau le plus proche."""
        # Dans un cas réel, nous appellerions une API de données hydrologiques
        # Pour l'exemple, nous retournons des données simulées
        return {
            "level": np.random.uniform(0, 5),
            "trend": np.random.choice(["rising", "stable", "falling"]),
            "timestamp": datetime.now(),
            "source": "simulated_data"
        }

class FloodRiskService:
    def __init__(self):
        self.elevation_service = ElevationService()
        self.weather_service = WeatherService()
        self.water_service = WaterService()
        self.historical_service = HistoricalDataService()

    def analyze_risk(self, polygon_coords: list) -> dict:
        """Analyse le risque d'inondation pour une zone donnée."""
        # Calculer le centre du polygone
        polygon = ShapelyPolygon([(lon, lat) for lat, lon in polygon_coords])
        center = polygon.centroid

        # Récupérer les données
        elevation = self.elevation_service.get_elevation(center.y, center.x)
        slope = self.elevation_service.get_slope(center.y, center.x)
        weather = self.weather_service.get_weather_data(center.y, center.x)
        water = self.water_service.get_water_level(center.y, center.x)

        # Récupérer les données historiques
        historical_stats = self.historical_service.get_statistics(
            center.y, center.x
        )

        # Calculer les facteurs de risque
        elevation_risk = self._calculate_elevation_risk(elevation)
        slope_risk = self._calculate_slope_risk(slope)
        precipitation_risk = self._calculate_precipitation_risk(
            weather["precipitation"] if weather else 0
        )
        water_level_risk = self._calculate_water_level_risk(
            water["level"] if water else 0
        )

        # Combiner les facteurs avec des poids
        weights = {
            "elevation": 0.25,
            "slope": 0.15,
            "precipitation": 0.25,
            "water_level": 0.15,
            "historical": 0.20
        }

        # Calculer le risque historique
        historical_risk = self._calculate_historical_risk(historical_stats)

        total_risk = (
            weights["elevation"] * elevation_risk +
            weights["slope"] * slope_risk +
            weights["precipitation"] * precipitation_risk +
            weights["water_level"] * water_level_risk +
            weights["historical"] * historical_risk
        )

        # Utiliser le modèle de prédiction
        prediction_risk = self.historical_service.predict_flood_risk({
            "elevation": elevation,
            "slope": slope,
            "precipitation": weather["precipitation"] if weather else 0,
            "water_level": water["level"] if water else 0
        })

        # Combiner le risque calculé avec la prédiction
        final_risk = 0.7 * total_risk + 0.3 * prediction_risk

        # Déterminer le niveau de risque
        if final_risk < 0.3:
            risk_level = "faible"
        elif final_risk < 0.6:
            risk_level = "moyen"
        else:
            risk_level = "élevé"

        # Calculer la proximité à l'eau (simulé pour l'exemple)
        water_proximity = np.random.uniform(0, 1)

        # Déterminer le type de sol (simulé pour l'exemple)
        soil_types = ["argile", "sable", "limon", "roche"]
        soil_type = np.random.choice(soil_types)

        # Déterminer l'utilisation du sol (simulé pour l'exemple)
        land_uses = ["urbain", "agricole", "forestier", "naturel"]
        land_use = np.random.choice(land_uses)

        return {
            "risk_score": final_risk,
            "risk_level": risk_level,
            "factors": {
                "elevation": elevation,
                "slope": slope,
                "precipitation": weather["precipitation"] if weather else 0,
                "water_level": water["level"] if water else 0,
                "water_proximity": water_proximity,
                "soil_type": soil_type,
                "land_use": land_use
            },
            "timestamp": datetime.now(),
            "confidence": self._calculate_confidence(
                weather, water, historical_stats
            )
        }

    def _calculate_elevation_risk(self, elevation: float) -> float:
        """Calcule le risque basé sur l'élévation."""
        return max(0, min(1, 1 - (elevation / 100)))

    def _calculate_slope_risk(self, slope: float) -> float:
        """Calcule le risque basé sur la pente."""
        return max(0, min(1, 1 - (slope / 45)))

    def _calculate_precipitation_risk(self, precipitation: float) -> float:
        """Calcule le risque basé sur les précipitations."""
        return max(0, min(1, precipitation / 50))

    def _calculate_water_level_risk(self, water_level: float) -> float:
        """Calcule le risque basé sur le niveau d'eau."""
        return max(0, min(1, water_level / 5))

    def _calculate_historical_risk(self, stats: dict) -> float:
        """Calcule le risque basé sur les données historiques."""
        if stats["total_floods"] == 0:
            return 0.0

        # Facteurs de risque historiques
        severity_weights = {"low": 0.3, "medium": 0.6, "high": 0.9}
        frequency_weight = min(1.0, stats["flood_frequency"] / 10)
        
        # Calculer le risque basé sur la sévérité moyenne
        severity_risk = severity_weights[stats["average_severity"]]
        
        # Combiner les facteurs
        return 0.7 * severity_risk + 0.3 * frequency_weight

    def _calculate_confidence(
        self, weather: dict, water: dict, historical: dict
    ) -> float:
        """Calcule le niveau de confiance de l'analyse."""
        confidence_factors = []

        # Qualité des données météo
        if weather:
            confidence_factors.append(0.9)
        else:
            confidence_factors.append(0.5)

        # Qualité des données hydrologiques
        if water and water["source"] != "simulated_data":
            confidence_factors.append(0.9)
        else:
            confidence_factors.append(0.6)

        # Qualité des données historiques
        if historical["total_floods"] > 10:
            confidence_factors.append(0.9)
        elif historical["total_floods"] > 0:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.5)

        return sum(confidence_factors) / len(confidence_factors) 