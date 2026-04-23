from typing import Any, Dict
from .base import BaseAgent
from app.services.weather import get_current_weather

class WeatherRiskAgent(BaseAgent):
    """
    Agent responsible for analyzing weather risks.
    Input: Location (Lat, Lon) or Explicit Weather Data
    Output: Risk Level, Advice
    """
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data: {
                "lat": float,
                "lon": float,
                "humidity": float (optional),
                "temperature": float (optional),
                "rain_forecast": bool (optional)
            }
        """
        lat = input_data.get("lat")
        lon = input_data.get("lon")
        
        # Use explicit data if available, else fetch
        humidity = input_data.get("humidity")
        temp = input_data.get("temperature")
        rain = input_data.get("rain_forecast")
        
        if humidity is None or temp is None:
             # Fetch real weather
             weather_data = get_current_weather(lat, lon)
             if "main" in weather_data:
                 main = weather_data.get("main", {})
                 fetched_temp = main.get("temp")
                 fetched_hum = main.get("humidity")
                 
                 if temp is None: temp = fetched_temp
                 if humidity is None: humidity = fetched_hum
                 
                 # Simple check for rain in description
                 weather_desc = weather_data.get("weather", [{}])[0].get("main", "")
                 if rain is None:
                    rain = "Rain" in weather_desc
        
        # Default fallbacks (handles both None from input and None from API failure)
        if humidity is None: humidity = 60.0
        if temp is None: temp = 25.0
        if rain is None: rain = False
        
        # Risk Logic
        risk_level = "Low"
        advice = "Weather is favorable."
        
        if humidity > 80:
            risk_level = "High"
            advice = "High humidity increases fungal spread. Avoid overhead watering."
        elif humidity > 60 and rain:
            risk_level = "High"
            advice = "Rain anticipated. Apply systemic fungicide if not done recently."
        elif humidity > 60:
            risk_level = "Moderate"
            advice = "Monitor for early signs of disease."
            
        return {
            "risk_level": risk_level,
            "spray_advice": advice,
            "current_weather": {
                "temp": temp,
                "humidity": humidity,
                "rain_expected": rain
            }
        }
