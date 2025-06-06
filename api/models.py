from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Coordinates(BaseModel):
    lat: float
    lon: float

class Polygon(BaseModel):
    coordinates: List[Coordinates]

class FloodRiskFactors(BaseModel):
    elevation: float
    water_proximity: float
    slope: float
    precipitation: float
    soil_type: str
    land_use: str

class FloodRiskAnalysis(BaseModel):
    polygon: Polygon
    risk_score: float
    risk_level: str
    factors: FloodRiskFactors
    timestamp: datetime
    confidence: float

class WeatherData(BaseModel):
    temperature: float
    precipitation: float
    humidity: float
    wind_speed: float
    timestamp: datetime

class WaterLevelData(BaseModel):
    level: float
    trend: str  # "rising", "stable", "falling"
    timestamp: datetime
    source: str 