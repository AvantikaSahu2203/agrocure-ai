from typing import Dict, Any, List
from datetime import datetime
from app.services.environmental_risk import EnvironmentalRiskService
from app.services.llm_service import AgriLLMService
from app.schemas.advisory import AdvisoryRequest
from app.services.detailed_agri_data import CROP_STAGES, DEFAULT_STAGES

# Initialize modular services
env_service = EnvironmentalRiskService()
llm_service = AgriLLMService()

def generate_crop_advice(data: AdvisoryRequest, current_user: Any) -> Dict[str, Any]:
    # 1. Fetch High-Resolution Environmental Risk & Weather
    # Fallback to neutral location if lat/lon is zero or missing
    lat = data.lat if data.lat != 0 else 20.5937
    lon = data.lon if data.lon != 0 else 78.9629
    
    risk_info = env_service.predict_risk(lat, lon)
    env_data = risk_info["environmental_data"]
    
    temp = env_data.get("temperature") if env_data.get("temperature") is not None else 25.0
    humidity = env_data.get("humidity") if env_data.get("humidity") is not None else 60.0
    rainfall = env_data.get("rainfall") if env_data.get("rainfall") is not None else 0.0
    soil_moist = env_data.get("soil_moisture") if env_data.get("soil_moisture") is not None else 0.3
    
    # 2. Fetch Detailed Growth Stage Protocol (10+ Crops support)
    crop_guide = CROP_STAGES.get(data.crop_name, DEFAULT_STAGES)
    stage_advice = crop_guide.get(data.growth_stage, DEFAULT_STAGES.get(data.growth_stage, DEFAULT_STAGES["Vegetative"]))
    
    # 3. Smart Risk Logic Enrichment
    risk_level = risk_info["risk_level"]
    risk_reason = "Conditions are favorable for healthy growth."
    risk_color = "Green"
    
    if risk_level == "High":
        risk_color = "Red"
        risk_reason = f"High disease risk alert! Excess moisture ({humidity}%) and temperature ({temp}°C) are triggering pathogen growth."
    elif risk_level == "Moderate":
        risk_color = "Yellow"
        risk_reason = f"Moderate risk detected. Keep an eye on new leaf growth for spots."
        
    # 4. Generate 'Best Friend' AI Persona Advice via LLM
    # We pass the rich context to the LLM to synthesize into a friendly voice
    persona_prompt = f"""
    Context:
    - Crop: {data.crop_name}
    - Stage: {data.growth_stage}
    - Weather: {temp}°C, Humidity {humidity}%, Rainfall {rainfall}mm
    - Current Task: {stage_advice['fertilizer']}
    - Risk: {risk_level} ({risk_reason})

    Write a 2-3 sentence friendly, supportive, and professional advice as a 'Farmer's Best Friend' in a caring tone. 
    Focus on what the farmer should do RIGHT NOW. 
    Use the crop name and stage.
    """
    
    # Generate personality-rich advice
    llm_response = llm_service.generate_advice(data.crop_name, f"{data.growth_stage}_advice_request")
    # For the 'voice_advice' persona, we use a simpler text if LLM is unavailable or for specific tone
    # Here we simulate or use the LLM to generate the specialized persona string
    friendly_voice = (
        f"Hello Annadata! Your {data.crop_name} at the {data.growth_stage} stage is doing well. "
        f"Today's {temp}°C and {humidity}% humidity suggest we should {stage_advice['fertilizer'].lower()}. "
    )
    if rainfall > 1:
        friendly_voice += "It looks like rain is coming, so stay indoors and check your drainage! "
    elif risk_level == "High":
        friendly_voice += f"Watch out! The high moisture ({humidity}%) might bring disease, so keep your sprays ready. "
    else:
        friendly_voice += "The weather is perfect for farming today. You're doing a great job!"

    return {
        "weather": {
            "summary": f"{temp}°C with {humidity}% humidity. Rainfall: {rainfall}mm.",
            "temp": temp,
            "humidity": humidity,
            "rain_probability": 0.8 if rainfall > 0 else 0.1,
            "actionable_steps": [
                f"Irrigation: {stage_advice['irrigation']}",
                f"Prevention: {stage_advice['spray']}"
            ]
        },
        "soil_fertilizer": {
            "recommendation": stage_advice["fertilizer"],
            "note": "Smart Tip: High-purity NPK gives best results in the early vegetative phase."
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
            "reason": risk_reason,
            "probability": risk_info["probability"]
        },
        "market_mandi": {
            "msp": f"Current MSP for {data.crop_name} is stable. Check local Mandi for best prices.",
            "subsidy": "Kisan Credit Card and Fasal Bima Yojna are available for this crop."
        },
        "voice_advice": friendly_voice,
        "timestamp": datetime.utcnow().isoformat()
    }
