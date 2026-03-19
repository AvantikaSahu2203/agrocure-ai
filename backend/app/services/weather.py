import requests
from app.core.config import settings

def get_current_weather(lat: float, lon: float):
    # This is a sample implementation. Ideally use async client like httpx.
    # For now synchronous requests is fine for MVP.
    if not settings.OPENWEATHER_API_KEY:
        return {"error": "OpenWeather API Key not configured"}
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

from app.schemas.weather_risk import WeatherRiskRequest

def analyze_weather_risk(data: WeatherRiskRequest) -> dict:
    """
    Analyze weather risk based on crop, humidity, rain forecast, and temperature.
    Using simple rule-based logic for MVP.
    """
    humidity = data.humidity
    rain_forecast = data.rain_forecast
    temperature = data.temperature
    
    # logic
    risk_level = "Low"
    alert_level = "Green"
    advice = "No immediate action needed."
    
    # High Risk Conditions
    if humidity > 80 or (rain_forecast and humidity > 70):
        risk_level = "High"
        alert_level = "Red"
        advice = "High fungal infection risk. Spray immediately if not raining. Avoid overhead irrigation."
    
    # Medium Risk Conditions
    elif humidity > 60 or rain_forecast:
        risk_level = "Medium"
        alert_level = "Yellow"
        advice = "Moderate risk. Monitor crops closely for symptoms. Ensure good drainage."
        
    return {
        "infection_risk_level": risk_level,
        "spraying_advice": advice,
        "alert_level": alert_level
    }

