import requests
from app.core.config import settings

def geocode_address(address: str):
    if not settings.GOOGLE_MAPS_API_KEY:
        return {"error": "Google Maps API Key not configured"}
    
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={settings.GOOGLE_MAPS_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
