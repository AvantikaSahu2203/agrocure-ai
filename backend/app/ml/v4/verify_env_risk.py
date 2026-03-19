import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.curdir))

from app.services.environmental_risk import EnvironmentalRiskService

def test_environmental_prediction():
    print("--- Environmental Risk Verification ---")
    
    # Mumbai coordinates
    lat, lon = 19.0760, 72.8777
    
    service = EnvironmentalRiskService()
    
    print(f"Testing location: {lat}, {lon}")
    result = service.predict_risk(lat, lon)
    
    print("\nResult:")
    print(f"Probability: {result['probability']}%")
    print(f"Risk Level: {result['risk_level']}")
    
    env_data = result['environmental_data']
    print("\nMeteorological Data:")
    print(f"Temperature: {env_data['temperature']}C")
    print(f"Humidity: {env_data['humidity']}%")
    print(f"Rainfall: {env_data['rainfall']}mm")
    print(f"Soil Moisture: {env_data['soil_moisture']}")
    
    if "error" in env_data:
        print(f"\nWARNING: API error detected: {env_data['error']}")
    else:
        print("\nAPI Integration: SUCCESS")

if __name__ == "__main__":
    test_environmental_prediction()
