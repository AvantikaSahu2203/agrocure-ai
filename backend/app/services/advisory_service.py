from typing import Dict, Any, List
from datetime import datetime
from app.services.weather import get_current_weather
from app.schemas.advisory import AdvisoryRequest

def generate_crop_advice(data: AdvisoryRequest) -> Dict[str, Any]:
    # 1. Fetch Weather
    weather_data = get_current_weather(data.lat, data.lon)
    
    # Defaults
    temp = weather_data.get("main", {}).get("temp", 25)
    humidity = weather_data.get("main", {}).get("humidity", 60)
    weather_main = weather_data.get("weather", [{}])[0].get("main", "Clear")
    
    # 2. Weather Advisory Logic
    actionable_steps: List[str] = []
    
    weather_advice = {
        "summary": f"Current weather is {weather_main} with {temp}°C.",
        "temp": temp,
        "humidity": humidity,
        "rain_probability": 0.8 if "Rain" in weather_main else 0.1,
        "actionable_steps": actionable_steps
    }
    
    if "Rain" in weather_main:
        actionable_steps.append("Postpone any planned fungicide sprays.")
        actionable_steps.append("Ensure proper drainage in the field.")
    elif temp > 35:
        actionable_steps.append("Increase irrigation frequency due to high temperature.")
    elif humidity > 80:
        actionable_steps.append("High humidity detected. Watch for fungal symptoms.")

    # 3. Growth Stage Logic (ICAR based mocks)
    growth_data = {
        "Seedling": {
            "fertilizer": "Apply starter dose of NPK (19:19:19) @ 2kg/acre.",
            "irrigation": "Maintain light moisture, avoid waterlogging.",
            "spray": "Preventive spray of Neem Oil if pests are visible."
        },
        "Vegetative": {
            "fertilizer": "Top dress with Urea @ 50kg/acre.",
            "irrigation": "Regular irrigation every 3-5 days.",
            "spray": "Foliar spray of Micronutrients."
        },
        "Flowering": {
            "fertilizer": "Apply Potash for better flower retention.",
            "irrigation": "Crucial stage: Ensure no water stress.",
            "spray": "Boric acid spray (1g/L) to improve fruit set."
        },
        "Harvest": {
            "fertilizer": "No fertilizer required now.",
            "irrigation": "Reduce irrigation 10 days before harvest.",
            "spray": "Stop all chemical sprays at least 15 days before harvest."
        }
    }
    
    stage_advice = growth_data.get(data.growth_stage, growth_data["Vegetative"])

    # 4. Disease Risk Prediction
    risk_level = "Low"
    risk_color = "Green"
    risk_reason = "Environmental conditions are stable."
    
    if humidity > 85 and temp < 20:
        risk_level = "High"
        risk_color = "Red"
        risk_reason = "High humidity and cool weather are ideal for Blight pathogens."
    elif humidity > 70:
        risk_level = "Medium"
        risk_color = "Yellow"
        risk_reason = "Moderate humidity increases risk of fungal leaf spots."

    # 5. Voice Advisory Text
    voice_msg = f"Current stage for your {data.crop_name} is {data.growth_stage}. "
    if "Rain" in weather_main:
        voice_msg += "Agle kuch ghanto me barish ki sambhavna hai, kripya sinchai aur dawai ka chidkao rokein. "
    else:
        voice_msg += f"Mausam saaf hai. {stage_advice['fertilizer']} "

    return {
        "weather": weather_advice,
        "soil_fertilizer": {
            "recommendation": stage_advice["fertilizer"],
            "soil_type_note": "Ensure soil testing every 2 years for optimized NPK usage."
        },
        "growth_stage_timeline": {
            "stage": data.growth_stage,
            "fertilizer_schedule": stage_advice["fertilizer"],
            "irrigation_schedule": stage_advice["irrigation"],
            "spray_schedule": stage_advice["spray"]
        },
        "disease_risk": {
            "level": risk_level,
            "color": risk_color,
            "reason": risk_reason
        },
        "market_mandi": {
            "msp": "MSP for current season is active. Check local mandi for daily rates.",
            "subsidy": "Fasal Bima Yojna registration is open."
        },
        "voice_advice": voice_msg,
        "timestamp": datetime.utcnow().isoformat()
    }
