from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models import Polygon, FloodRiskAnalysis, WeatherData, WaterLevelData
from services import FloodRiskService, WeatherService, WaterService
from historical_data import HistoricalDataService
import uvicorn

app = FastAPI(
    title="API d'Analyse de Risque d'Inondation",
    description="API pour l'analyse en temps réel des risques d'inondation",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation des services
flood_risk_service = FloodRiskService()
weather_service = WeatherService()
water_service = WaterService()

@app.get("/")
async def root():
    """
    Point d'entrée de l'API qui fournit des informations sur les endpoints disponibles.
    """
    return JSONResponse({
        "message": "Bienvenue sur l'API d'Analyse de Risque d'Inondation",
        "version": "1.0.0",
        "endpoints": {
            "analyze_risk": {
                "path": "/analyze-risk",
                "method": "POST",
                "description": "Analyse le risque d'inondation pour une zone donnée"
            },
            "weather": {
                "path": "/weather/{lat}/{lon}",
                "method": "GET",
                "description": "Récupère les données météorologiques pour un point donné"
            },
            "water_level": {
                "path": "/water-level/{lat}/{lon}",
                "method": "GET",
                "description": "Récupère le niveau d'eau le plus proche d'un point donné"
            },
            "docs": {
                "path": "/docs",
                "method": "GET",
                "description": "Documentation interactive de l'API (Swagger UI)"
            }
        }
    })

@app.post("/analyze-risk", response_model=FloodRiskAnalysis)
async def analyze_flood_risk(polygon: Polygon):
    """
    Analyse le risque d'inondation pour une zone donnée.
    
    Args:
        polygon: Coordonnées du polygone à analyser
        
    Returns:
        FloodRiskAnalysis: Résultat de l'analyse avec score de risque
    """
    try:
        # Convertir les coordonnées en format attendu par le service
        coords = [[coord.lat, coord.lon] for coord in polygon.coordinates]
        
        # Analyser le risque
        result = flood_risk_service.analyze_risk(coords)
        
        return FloodRiskAnalysis(
            polygon=polygon,
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            factors=result["factors"],
            timestamp=result["timestamp"],
            confidence=result["confidence"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather/{lat}/{lon}", response_model=WeatherData)
async def get_weather(lat: float, lon: float):
    """
    Récupère les données météorologiques pour un point donné.
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        WeatherData: Données météorologiques actuelles
    """
    try:
        weather_data = weather_service.get_weather_data(lat, lon)
        if not weather_data:
            raise HTTPException(
                status_code=404,
                detail="Données météo non trouvées"
            )
        return WeatherData(**weather_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/water-level/{lat}/{lon}", response_model=WaterLevelData)
async def get_water_level(lat: float, lon: float):
    """
    Récupère le niveau d'eau le plus proche d'un point donné.
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        WaterLevelData: Données sur le niveau d'eau
    """
    try:
        water_data = water_service.get_water_level(lat, lon)
        return WaterLevelData(**water_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True) 