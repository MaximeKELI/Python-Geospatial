import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict
import json
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


class HistoricalDataService:
    def __init__(self):
        self.data_file = "data/historical_floods.json"
        self.model = None
        self.scaler = StandardScaler()
        self._load_or_create_data()
        self._train_model()

    def _load_or_create_data(self):
        """Charge ou crée le fichier de données historiques."""
        if not os.path.exists(self.data_file):
            # Créer des données historiques fictives
            data = {
                "floods": [
                    {
                        "date": (
                            datetime.now() - timedelta(days=i)
                        ).isoformat(),
                        "location": {
                            "lat": 48.8566 + np.random.uniform(-0.1, 0.1),
                            "lon": 2.3522 + np.random.uniform(-0.1, 0.1)
                        },
                        "severity": np.random.choice(
                            ["low", "medium", "high"]
                        ),
                        "factors": {
                            "elevation": np.random.uniform(0, 100),
                            "slope": np.random.uniform(0, 45),
                            "precipitation": np.random.uniform(0, 100),
                            "water_level": np.random.uniform(0, 5)
                        }
                    }
                    for i in range(1000)  # 1000 événements historiques
                ]
            }
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump(data, f)
        
        with open(self.data_file, 'r') as f:
            self.data = json.load(f)

    def _train_model(self):
        """Entraîne le modèle de prédiction sur les données historiques."""
        # Préparer les données d'entraînement
        X = []
        y = []
        
        for flood in self.data["floods"]:
            factors = flood["factors"]
            X.append([
                factors["elevation"],
                factors["slope"],
                factors["precipitation"],
                factors["water_level"]
            ])
            y.append(1 if flood["severity"] in ["medium", "high"] else 0)
        
        X = np.array(X)
        y = np.array(y)
        
        # Normaliser les données
        X = self.scaler.fit_transform(X)
        
        # Entraîner le modèle
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)

    def get_historical_floods(
        self, lat: float, lon: float, radius_km: float = 10
    ) -> List[Dict]:
        """Récupère les inondations historiques dans un rayon donné."""
        from geopy.distance import geodesic
        
        center = (lat, lon)
        historical_floods = []
        
        for flood in self.data["floods"]:
            flood_loc = (flood["location"]["lat"], flood["location"]["lon"])
            distance = geodesic(center, flood_loc).kilometers
            
            if distance <= radius_km:
                historical_floods.append(flood)
        
        return historical_floods

    def predict_flood_risk(self, factors: Dict) -> float:
        """Prédit le risque d'inondation basé sur les facteurs actuels."""
        # Préparer les données
        X = np.array([[
            factors["elevation"],
            factors["slope"],
            factors["precipitation"],
            factors["water_level"]
        ]])
        
        # Normaliser les données
        X = self.scaler.transform(X)
        
        # Faire la prédiction
        probability = self.model.predict_proba(X)[0][1]
        return float(probability)

    def get_statistics(
        self, lat: float, lon: float, radius_km: float = 10
    ) -> Dict:
        """Récupère les statistiques des inondations historiques."""
        floods = self.get_historical_floods(lat, lon, radius_km)
        
        if not floods:
            return {
                "total_floods": 0,
                "average_severity": "none",
                "last_flood": None,
                "flood_frequency": 0
            }
        
        # Calculer les statistiques
        total_floods = len(floods)
        severity_counts = {"low": 0, "medium": 0, "high": 0}
        
        for flood in floods:
            severity_counts[flood["severity"]] += 1
        
        # Calculer la sévérité moyenne
        severity_scores = {"low": 1, "medium": 2, "high": 3}
        avg_severity_score = sum(
            severity_scores[flood["severity"]] for flood in floods
        ) / total_floods
        
        if avg_severity_score < 1.5:
            avg_severity = "low"
        elif avg_severity_score < 2.5:
            avg_severity = "medium"
        else:
            avg_severity = "high"
        
        # Trouver la dernière inondation
        last_flood = max(
            floods,
            key=lambda x: datetime.fromisoformat(x["date"])
        )
        
        # Calculer la fréquence (inondations par an)
        first_date = datetime.fromisoformat(
            min(floods, key=lambda x: x["date"])["date"]
        )
        last_date = datetime.fromisoformat(last_flood["date"])
        years = (last_date - first_date).days / 365.25
        flood_frequency = total_floods / years if years > 0 else 0
        
        return {
            "total_floods": total_floods,
            "average_severity": avg_severity,
            "last_flood": last_flood,
            "flood_frequency": flood_frequency,
            "severity_distribution": severity_counts
        } 