import sys
import os

# Add the app directory to sys.path
cwd = os.getcwd()
sys.path.append(cwd)

from app.services.environmental_risk import EnvironmentalRiskService

def debug():
    service = EnvironmentalRiskService()
    # Coordinates for Pune, India
    lat, lon = 18.5204, 73.8567
    print(f"Testing reach for lat={lat}, lon={lon}")
    
    try:
        data = service.fetch_environmental_data(lat, lon)
        print("\n[Environmental Data Output]")
        print(data)
        
        risk = service.predict_risk(lat, lon)
        print("\n[Predict Risk Output]")
        print(risk)
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug()
