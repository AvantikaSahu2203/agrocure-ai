import requests
import numpy as np
import os
import joblib
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta

class EnvironmentalRiskService:
    """
    Predicts disease risk based on environmental data from Open-Meteo API.
    """
    API_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, model_path: str = "app/ml/v4/env_risk_rf.joblib"):
        self.model_path = model_path
        self.model = self._load_model()

    def _load_model(self):
        """Loads the pre-trained Random Forest model."""
        if os.path.exists(self.model_path):
            try:
                return joblib.load(self.model_path)
            except Exception as e:
                print(f"Error loading environmental model: {e}")
        return None

    def fetch_environmental_data(self, lat: float, lon: float) -> Dict:
        """Fetch current and recent meteorological data from Open-Meteo."""
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,relative_humidity_2m,precipitation,soil_moisture_0_to_1cm",
            "current_weather": "true",
            "timezone": "auto",
            "past_days": 1
        }
        
        try:
            response = requests.get(self.API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extract current values
            current = data.get("current_weather", {})
            hourly = data.get("hourly", {})
            
            # Get latest values from hourly data
            latest_idx = -1
            features = {
                "temperature": current.get("temperature", 25.0),
                "humidity": hourly.get("relative_humidity_2m", [60.0])[latest_idx],
                "rainfall": hourly.get("precipitation", [0.0])[latest_idx],
                "soil_moisture": hourly.get("soil_moisture_0_to_1cm", [0.3])[latest_idx]
            }
            return features
        except Exception as e:
            print(f"Error fetching Open-Meteo data: {e}")
            return {
                "temperature": 25.0,
                "humidity": 60.0,
                "rainfall": 0.0,
                "soil_moisture": 0.3,
                "error": str(e)
            }

    def predict_risk(self, lat: float, lon: float) -> Dict:
        """Calculate disease risk score and level."""
        features = self.fetch_environmental_data(lat, lon)
        
        # Feature vector for model: [temp, humidity, rain, soil_moisture]
        X = np.array([[
            features["temperature"],
            features["humidity"],
            features["rainfall"],
            features["soil_moisture"]
        ]])

        if self.model:
            # Probability of "High Risk" (assuming binary classification for now)
            prob = self.model.predict_proba(X)[0][1] * 100
        else:
            # Fallback to smart rule-based logic if model isn't trained
            prob = self._heuristic_risk(features)

        risk_level = "Low"
        if prob > 70:
            risk_level = "High"
        elif prob > 30:
            risk_level = "Moderate"

        return {
            "probability": round(float(prob), 2),
            "risk_level": risk_level,
            "environmental_data": features,
            "location": {"lat": lat, "lon": lon}
        }

    def _heuristic_risk(self, f: Dict) -> float:
        """Heuristic calculation for risk if ML model is unavailable."""
        score = 0
        # Humidity is a major factor for fungal disease
        if f["humidity"] > 85: score += 40
        elif f["humidity"] > 70: score += 20
        
        # Rainfall increases risk
        if f["rainfall"] > 5: score += 30
        elif f["rainfall"] > 0: score += 15
        
        # High soil moisture
        if f["soil_moisture"] > 0.4: score += 20
        
        # Temperature (20-30C is prime for most pathogens)
        if 20 <= f["temperature"] <= 32:
            score += 10
            
        return min(score, 100)

if __name__ == "__main__":
    # Test
    service = EnvironmentalRiskService()
    print(service.predict_risk(19.0760, 72.8777)) # Mumbai coordinates
