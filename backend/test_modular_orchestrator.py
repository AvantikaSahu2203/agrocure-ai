import asyncio
from app.services.orchestrator_service import AIOrchestrator
import json

async def test_orchestrator():
    orchestrator = AIOrchestrator()
    
    # Mock data
    with open("test_image.jpg", "rb") as f:
        image_data = f.read()
        
    location_data = {
        "city": "Mumbai",
        "state": "Maharashtra",
        "lat": 19.076,
        "lon": 72.877,
        "humidity": 75.0,
        "temperature": 28.0,
        "rain_forecast": False
    }
    
    try:
        from app.db.session import SessionLocal
        from app.models.disease import DiseaseDetection, DetectionStatus
        from app.models.user import User
        import uuid
        
        db = SessionLocal()
        current_user = db.query(User).first()
        if not current_user:
             print("FAILED: No user found in DB to test with.")
             return

        print(f"Starting Analysis for {current_user.email}...")
        result = orchestrator.perform_full_analysis(
            image_data=image_data,
            crop_name="Tomato",
            location_data=location_data
        )
        print("Analysis Successful!")
        
        disease_analysis = result["disease_analysis"]
        medicine = result["medicine_recommendations"]
        
        disease_analysis["confidence"] = disease_analysis.get("confidence", 0.0)
        disease_analysis["chemical_treatment"] = medicine["chemical_treatment"]
        disease_analysis["organic_treatment"] = medicine["organic_treatment"]
        disease_analysis["dosage"] = medicine["dosage"]
        disease_analysis["recommendations"] = medicine["preventative_measures"]

        ecommerce_links = result["ecommerce_links"]
        ecommerce_links["google_search_url"] = ecommerce_links["maps_url"]

        weather_risk = result["weather_risk"]
        weather_risk["infection_risk_level"] = weather_risk["risk_level"]
        weather_risk["spraying_advice"] = weather_risk["spray_advice"]

        print("Mapping Successful!")

        # Save to DB
        mock_image_url = f"uploads/{uuid.uuid4()}.jpg"
        db_detection = DiseaseDetection(
            user_id=current_user.id,
            image_url=mock_image_url,
            detected_disease=disease_analysis.get("disease_name"),
            confidence_score=disease_analysis.get("confidence"),
            details={
                "analysis": disease_analysis,
                "weather_risk": weather_risk,
                "ecommerce": ecommerce_links,
                "full_agent_report": result
            },
            status=DetectionStatus.COMPLETED
        )
        db.add(db_detection)
        db.commit()
        print(f"DB Save Successful! Report ID: {db_detection.id}")
        db.close()
        
    except Exception as e:
        import traceback
        print(f"FAILED: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_orchestrator())
