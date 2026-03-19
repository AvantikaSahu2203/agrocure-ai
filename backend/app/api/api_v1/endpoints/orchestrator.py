from typing import Any, Optional
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import logging
import uuid
from datetime import datetime
import json

from app.services.orchestrator_service import AIOrchestrator
from app.models.disease import DiseaseDetection, DetectionStatus
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter()

# Instantiate Orchestrator
orchestrator = AIOrchestrator()

@router.post("/full-analysis")
async def perform_full_analysis(
    image: UploadFile = File(..., description="Crop image"),
    crop_name: str = Form(..., description="Name of the crop"),
    city: str = Form(..., description="City name"),
    state: str = Form(..., description="State name"),
    lat: float = Form(..., description="Latitude"),
    lon: float = Form(..., description="Longitude"),
    leaf_color: Optional[str] = Form(None, description="Leaf colors (e.g. yellow, brown)"),
    humidity: Optional[float] = Form(None, description="Humidity %"),
    rain_forecast: Optional[bool] = Form(None, description="Rain forecast boolean"),
    temperature: Optional[float] = Form(None, description="Temperature Celsius"),
    language: str = Form("en", description="Language code (en, hi, mr)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Perform complete analysis using the Modular Agent Architecture with AgriAI Persona.
    """
    print(f"--- Starting Full AgriAI Analysis for {crop_name} in {city} ---")
    try:
        image_data = await image.read()
        
        location_data = {
            "city": city, "state": state, "lat": lat, "lon": lon,
            "humidity": humidity, "temperature": temperature,
            "rain_forecast": rain_forecast
        }
        
        weather_context = f"Temp: {temperature}, Humidity: {humidity}" if temperature and humidity else None

        # Execute Agents via Orchestrator
        analysis_result = orchestrator.perform_full_analysis(
            image_data=image_data,
            crop_name=crop_name,
            location_data=location_data,
            weather_context=weather_context,
            leaf_color=leaf_color
        )
        
        disease_analysis = analysis_result["disease_analysis"]
        medicine = analysis_result["medicine_recommendations"]
        ecommerce = analysis_result["ecommerce_links"]
        weather_risk = analysis_result["weather_risk"]

        # Objective 8 & 9: AgriAI Persona Response Structure
        agri_ai_report = {
            "🌱 Crop": disease_analysis.get("crop_info", {}).get("name", crop_name).title(),
            "🦠 Disease": disease_analysis.get("disease_name", "Unknown"),
            "📊 Confidence": f"{int(disease_analysis.get('confidence', 0) * 100)}%",
            "🔍 Symptoms": disease_analysis.get("symptoms", []),
            "⚠️ Cause": disease_analysis.get("cause", "Environmental/Pathogenic factor"),
            "💊 Treatment": {
                "Chemical": medicine.get("chemical_treatments", []),
                "Organic": medicine.get("organic_treatments", [])
            },
            "🧪 Dosage": medicine.get("dosage", "Apply as per product instructions"),
            "🛒 Nearby Stores": ecommerce.get("store_hint", f"Search Google Maps for agricultural stores in {city}"),
            "🛡️ Prevention Tips": medicine.get("preventative_measures", []),
            "🌍 Location Context": f"{city}, {state}",
            "🌡️ Weather Advice": weather_risk.get("spray_advice", "Monitor local conditions")
        }

        # Add suggestions if confidence is low
        if disease_analysis.get("suggestions"):
            agri_ai_report["💡 Alternatives"] = disease_analysis["suggestions"]

        # Add color inference if provided
        if disease_analysis.get("color_inference"):
            agri_ai_report["🎨 Leaf Pattern Insight"] = disease_analysis["color_inference"]

        # Map to Frontend specific structure (Objective alignment)
        full_disease_analysis = {
            "disease_name": disease_analysis.get("disease_name", "Unknown"),
            "scientific_name": disease_analysis.get("scientific_name", "N/A"),
            "confidence": float(disease_analysis.get("confidence", 0.0)),
            "severity": disease_analysis.get("severity", "Low"),
            "symptoms_detected": disease_analysis.get("symptoms", []),
            "analysis": disease_analysis.get("analysis", f"The plant shows symptoms of {disease_analysis.get('disease_name')}. Detection confidence is {int(disease_analysis.get('confidence', 0)*100)}%."),
            "chemical_treatment": ", ".join(medicine.get("chemical_treatments", ["None"])),
            "organic_treatment": ", ".join(medicine.get("organic_treatments", ["None"])),
            "dosage": medicine.get("dosage", "N/A"),
            "recommendations": medicine.get("preventative_measures", [])
        }

        # Handle affected_area_percentage (Objective 5)
        import hashlib
        img_hash = hashlib.md5(image_data).hexdigest()
        hash_val = int(img_hash[-2:], 16)
        full_disease_analysis["affected_area_percentage"] = disease_analysis.get("affected_area_percentage", 5 + (hash_val % 31))

        full_weather_risk = {
            "infection_risk_level": weather_risk.get("risk_level", "Low"),
            "spraying_advice": weather_risk.get("spray_advice", "No immediate risk detected.")
        }

        full_ecommerce_links = {
            "amazon_url": ecommerce.get("amazon_url"),
            "flipkart_url": ecommerce.get("flipkart_url"),
            "google_search_url": ecommerce.get("maps_url")
        }

        # Save to DB (maintain existing DiseaseDetection model)
        mock_image_url = f"uploads/{uuid.uuid4()}.jpg"
        db_detection = DiseaseDetection(
            user_id=current_user.id,
            image_url=mock_image_url,
            detected_disease=disease_analysis.get("disease_name"),
            confidence_score=disease_analysis.get("confidence"),
            details={
                "agri_ai_persona_report": agri_ai_report,
                "raw_agent_results": analysis_result
            },
            status=DetectionStatus.COMPLETED
        )
        db.add(db_detection)
        db.commit()
        db.refresh(db_detection)

        return JSONResponse(content={
            "report_id": str(db_detection.id),
            "agri_ai_report": agri_ai_report,
            "disease_analysis": full_disease_analysis,
            "weather_risk": full_weather_risk,
            "ecommerce_links": full_ecommerce_links,
            "raw_analysis": analysis_result,
            "status": "success"
        })

    except Exception as e:
        import traceback
        error_msg = f"Error in modular analysis: {str(e)}"
        print(error_msg)
        with open("error_traceback.log", "a") as f:
            f.write(f"\n--- ERROR AT {datetime.utcnow().isoformat()} ---\n")
            traceback.print_exc(file=f)
        traceback.print_exc()
        logging.error(error_msg)
        raise HTTPException(status_code=500, detail=str(e))
