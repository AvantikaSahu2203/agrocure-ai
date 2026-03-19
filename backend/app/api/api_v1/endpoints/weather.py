from typing import Any

from fastapi import APIRouter, Depends, Query
from app.api import deps
from app.models import User
from app.services.weather import get_current_weather, analyze_weather_risk
from app.schemas.weather_risk import WeatherRiskRequest

router = APIRouter()

@router.get("/current")
def get_weather(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current weather for a location.
    """
    return get_current_weather(lat, lon)

@router.post("/predict-risk")
def predict_weather_risk(
    data: WeatherRiskRequest,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Predict crop infection risk based on weather conditions.
    """
    return analyze_weather_risk(data)
