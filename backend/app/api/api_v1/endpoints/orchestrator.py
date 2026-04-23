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

@router.post("/orchestrate")
async def perform_secure_analysis(
    image: UploadFile = File(..., description="Crop image"),
    crop_name: str = Form(..., description="Name of the crop"),
    city: str = Form("Unknown", description="City name"),
    state: str = Form("Unknown", description="State name"),
    lat: float = Form(20.5937, description="Latitude"),
    lon: float = Form(78.9629, description="Longitude"),
    leaf_color: Optional[str] = Form(None, description="Leaf colors (e.g. yellow, brown)"),
    humidity: Optional[float] = Form(None, description="Humidity %"),
    rain_forecast: Optional[bool] = Form(None, description="Rain forecast boolean"),
    temperature: Optional[float] = Form(None, description="Temperature Celsius"),
    language: str = Form("en", description="Language code (en, hi, mr)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    AgriAI Secure Analysis Endpoint.
    Requires a valid JWT token.
    """
    return await _execute_analysis_logic(
        image=image, crop_name=crop_name, city=city, state=state,
        lat=lat, lon=lon, leaf_color=leaf_color, humidity=humidity,
        rain_forecast=rain_forecast, temperature=temperature,
        language=language, db=db, user_id=current_user.id
    )

async def _execute_analysis_logic(
    image: UploadFile, crop_name: str, city: str, state: str,
    lat: float, lon: float, leaf_color: Optional[str], humidity: Optional[float],
    rain_forecast: Optional[bool], temperature: Optional[float],
    language: str, db: Session, user_id: str
) -> Any:
    """Internal helper to share logic between public and private endpoints."""
    print(f"--- Executing AgriAI Analysis (v7) for {crop_name} ---")
    try:
        image_data = await image.read()
        location_data = {
            "city": city, "state": state, "lat": lat, "lon": lon,
            "humidity": humidity, "temperature": temperature,
            "rain_forecast": rain_forecast
        }
        
        # Execute Agents via Orchestrator (Priority v7 engine)
        analysis_result = orchestrator.perform_full_analysis(
            image_data=image_data,
            crop_name=crop_name,
            location_data=location_data,
            leaf_color=leaf_color
        )
        
        disease_analysis = analysis_result["disease_analysis"]
        medicine = analysis_result["medicine_recommendations"]
        ecommerce = analysis_result["ecommerce_links"]
        weather_risk = analysis_result["weather_risk"]

        # AgriAI Persona Report Structure
        agri_ai_report = {
            "\U0001F331 Crop": disease_analysis.get("crop_info", {}).get("name", crop_name).title(),
            "\U0001F9A0 Disease": disease_analysis.get("disease_name", "Unknown"),
            "\U0001F4CA Confidence": f"{int(disease_analysis.get('confidence', 0) * 100)}%",
            "\U0001F50D Symptoms": disease_analysis.get("symptoms", []),
            "\u26A0\uFE0F Cause": disease_analysis.get("cause", "Environmental/Pathogenic factor"),
            "\U0001F48A Treatment": {
                "Chemical": medicine.get("chemical_treatments", []),
                "Organic": medicine.get("organic_treatments", [])
            },
            "\U0001F9EA Dosage": medicine.get("dosage", "Apply as per product instructions"),
            "\U0001F6E1\uFE0F Prevention Tips": medicine.get("preventative_measures", []),
            "\U0001F30D Location Context": f"{city}, {state}"
        }

        # 1. NEW: Upload to Supabase Storage (Cloud)
        from app.utils.storage import upload_image_to_cloud
        image_url = await upload_image_to_cloud(image_data)

        # Save to DB
        db_detection = DiseaseDetection(
            user_id=user_id,
            image_url=image_url,
            detected_disease=disease_analysis.get("disease_name"),
            confidence_score=disease_analysis.get("confidence"),
            details={"agri_ai_persona_report": agri_ai_report, "raw_agent_results": analysis_result},
            status=DetectionStatus.COMPLETED
        )
        db.add(db_detection)
        db.commit()
        db.refresh(db_detection)

        return JSONResponse(content={
            "report_id": str(db_detection.id),
            "agri_ai_report": agri_ai_report,
            "disease_analysis": {
                "disease_name": disease_analysis.get("disease_name", "Unknown"),
                "confidence": float(disease_analysis.get("confidence", 0.0)),
                "severity": disease_analysis.get("severity", "Medium"),
                "affected_area_percentage": disease_analysis.get("affected_area_percentage", 0),
                "scientific_name": disease_analysis.get("scientific_name", "N/A"),
                "analysis": disease_analysis.get("analysis", "No detailed analysis available."),
                "symptoms_detected": disease_analysis.get("symptoms", []),
                "chemical_treatment": ", ".join(medicine.get("chemical_treatments", ["None"])),
                "organic_treatment": ", ".join(medicine.get("organic_treatments", ["None"])),
                "dosage": medicine.get("dosage", "N/A"),
                "recommendations": medicine.get("preventative_measures", [])
            },
            "ecommerce_links": ecommerce,
            "weather_risk": weather_risk,
            "status": "success"
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/full-analysis")
async def perform_full_analysis(
    image: UploadFile = File(..., description="Crop image"),
    crop_name: str = Form(..., description="Name of the crop"),
    city: str = Form("Unknown", description="City name"),
    state: str = Form("Unknown", description="State name"),
    lat: float = Form(20.5937, description="Latitude"),
    lon: float = Form(78.9629, description="Longitude"),
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
    return await _execute_analysis_logic(
        image=image, crop_name=crop_name, city=city, state=state,
        lat=lat, lon=lon, leaf_color=leaf_color, humidity=humidity,
        rain_forecast=rain_forecast, temperature=temperature,
        language=language, db=db, user_id=current_user.id
    )
