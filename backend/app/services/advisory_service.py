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
    lat = data.lat if data.lat != 0 else 20.5937
    lon = data.lon if data.lon != 0 else 78.9629
    lang = data.language or "en"
    
    risk_info = env_service.predict_risk(lat, lon)
    env_data = risk_info["environmental_data"]
    
    temp = env_data.get("temperature") if env_data.get("temperature") is not None else 25.0
    humidity = env_data.get("humidity") if env_data.get("humidity") is not None else 60.0
    rainfall = env_data.get("rainfall") if env_data.get("rainfall") is not None else 0.0
    
    # 2. Fetch Detailed Growth Stage Protocol
    crop_guide = CROP_STAGES.get(data.crop_name, DEFAULT_STAGES)
    stage_advice = crop_guide.get(data.growth_stage, DEFAULT_STAGES.get(data.growth_stage, DEFAULT_STAGES["Vegetative"]))
    
    # 3. Smart Risk Logic Enrichment
    risk_level = risk_info["risk_level"]
    
    # Language Mapping for Core Strings
    TRANSLATIONS = {
        "hi": {
            "summary_template": "{temp}°C और {humidity}% आर्द्रता। वर्षा: {rainfall}मिमी।",
            "favorable": "स्थितियां स्वस्थ विकास के लिए अनुकूल हैं।",
            "high_risk": "बीमारी का उच्च जोखिम! अतिरिक्त नमी ({humidity}%) और तापमान ({temp}°C) रोगजनकों के विकास को बढ़ावा दे रहे हैं।",
            "moderate_risk": "मध्यम जोखिम पाया गया। धब्बों के लिए नई पत्तियों के विकास पर नज़र रखें।",
            "voice_start": "नमस्ते अन्नदाता! आपकी {crop_name} {growth_stage} चरण में अच्छा कर रही है। ",
            "voice_action": "आज का {temp}°C और {humidity}% आर्द्रता बताती है कि हमें {action} करना चाहिए। ",
            "rain_alert": "ऐसा लग रहा है कि बारिश आने वाली है, इसलिए घर के अंदर रहें और जल निकासी की जांच करें! ",
            "moisture_alert": "सावधान! उच्च नमी ({humidity}%) बीमारी ला सकती है, इसलिए अपने स्प्रे तैयार रखें। ",
            "perfect_weather": "आज खेती के लिए मौसम एकदम सही है। आप बहुत अच्छा काम कर रहे हैं!",
            "Low": "कम", "Moderate": "मध्यम", "High": "उच्च",
            "Seedling": "अंकुर", "Vegetative": "वानस्पतिक", "Flowering": "फूल", "Harvest": "कटाई"
        },
        "en": {
            "summary_template": "{temp}°C with {humidity}% humidity. Rainfall: {rainfall}mm.",
            "favorable": "Conditions are favorable for healthy growth.",
            "high_risk": "High disease risk alert! Excess moisture ({humidity}%) and temperature ({temp}°C) are triggering pathogen growth.",
            "moderate_risk": "Moderate risk detected. Keep an eye on new leaf growth for spots.",
            "voice_start": "Hello Annadata! Your {crop_name} at the {growth_stage} stage is doing well. ",
            "voice_action": "Today's {temp}°C and {humidity}% humidity suggest we should {action}. ",
            "rain_alert": "It looks like rain is coming, so stay indoors and check your drainage! ",
            "moisture_alert": "Watch out! The high moisture ({humidity}%) might bring disease, so keep your sprays ready. ",
            "perfect_weather": "The weather is perfect for farming today. You're doing a great job!"
        }
    }
    
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    
    risk_reason = t["favorable"]
    risk_color = "Green"
    
    if risk_level == "High":
        risk_color = "Red"
        risk_reason = t["high_risk"].format(temp=temp, humidity=humidity)
    elif risk_level == "Moderate":
        risk_color = "Yellow"
        risk_reason = t["moderate_risk"]
        
    # 4. Generate 'Best Friend' AI Persona Advice
    action_text = stage_advice['fertilizer'].lower()
    
    friendly_voice = t["voice_start"].format(crop_name=data.crop_name, growth_stage=t.get(data.growth_stage, data.growth_stage))
    friendly_voice += t["voice_action"].format(temp=temp, humidity=humidity, action=action_text)
    
    if rainfall > 1:
        friendly_voice += t["rain_alert"]
    elif risk_level == "High":
        friendly_voice += t["moisture_alert"].format(humidity=humidity)
    else:
        friendly_voice += t["perfect_weather"]

    return {
        "weather": {
            "summary": t["summary_template"].format(temp=temp, humidity=humidity, rainfall=rainfall),
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
            "note": "Smart Tip: High-purity NPK gives best results."
        },
        "growth_stage_timeline": {
            "stage": t.get(data.growth_stage, data.growth_stage),
            "fertilizer_schedule": stage_advice["fertilizer"],
            "irrigation_schedule": stage_advice["irrigation"],
            "spray_schedule": stage_advice["spray"]
        },
        "disease_risk": {
            "level": t.get(risk_level, risk_level),
            "color": risk_color,
            "reason": risk_reason,
            "probability": risk_info["probability"]
        },
        "market_mandi": {
            "msp": f"Current MSP for {data.crop_name} is stable.",
            "subsidy": "Kisan Credit Card and Fasal Bima Yojna are available."
        },
        "voice_advice": friendly_voice,
        "timestamp": datetime.utcnow().isoformat()
    }
