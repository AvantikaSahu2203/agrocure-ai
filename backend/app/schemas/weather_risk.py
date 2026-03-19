from pydantic import BaseModel
from typing import Optional

class WeatherRiskRequest(BaseModel):
    crop: str
    humidity: float
    rain_forecast: bool
    temperature: float

class WeatherRiskResponse(BaseModel):
    infection_risk_level: str  # Low, Medium, High
    spraying_advice: str
    alert_level: str  # Green, Yellow, Red
