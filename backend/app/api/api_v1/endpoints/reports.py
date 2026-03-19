from typing import Any, List, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.api.deps import get_db, get_current_user
from app.models.disease import DiseaseDetection
from app.models.user import User

router = APIRouter()

@router.get("/stats")
def get_report_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get aggregated statistics for the user's crop reports.
    """
    # Fetch all detections for the user
    detections = db.query(DiseaseDetection).filter(
        DiseaseDetection.user_id == current_user.id
    ).order_by(DiseaseDetection.created_at.desc()).all()
    
    total_scans = len(detections)
    
    # Calculate Diseases Found (excluding "Potential Fungal Infection" if generic, but usually specific)
    # And assuming "Healthy" is not a disease.
    unique_diseases = set()
    for d in detections:
        if d.detected_disease and "healthy" not in d.detected_disease.lower():
            unique_diseases.add(d.detected_disease)
            
    diseases_count = len(unique_diseases)
    
    # Calculate Crops Monitored
    unique_crops = set()
    for d in detections:
        if d.details and "analysis" in d.details and "crop_info" in d.details["analysis"]:
            crop_name = d.details["analysis"]["crop_info"].get("name")
            if crop_name:
                unique_crops.add(crop_name)
    
    crops_count = len(unique_crops)
    
    # Calculate Health Score
    healthy_count = 0
    for d in detections:
        if d.detected_disease and "healthy" in d.detected_disease.lower():
             healthy_count += 1
        # Also check if severity is 'low' or confidence is low? 
        # For now, let's rely on the disease name containing "Healthy" or if we have a specific "Healthy" class.
        # If the model returns "Tomato Early Blight", it's not healthy.
        # If we don't have an explicit "Healthy" class in our mock DB, 
        # we might need to assume anything not in the excluded list is disease.
        # Actually our mock DB *doesn't* have "Healthy" entries for crops usually, 
        # it returns a disease. 
        # So "Healthy" might be rare unless we implemented a 'Healthy' check.
        # Let's mock the health score for now based on severity 'low' = healthy-ish?
        # Or better: (1 - (High Severity Count / Total)) * 100
        pass

    # Severity based health score
    high_severity_count = 0
    for d in detections:
        # Check details for severity
        if d.details and "analysis" in d.details:
            severity = d.details["analysis"].get("severity", "").lower()
            if severity == "high" or severity == "severe":
                high_severity_count += 1
    
    health_score = 100
    if total_scans > 0:
        health_score = int(((total_scans - high_severity_count) / total_scans) * 100)

    # Recent Activity (Top 5)
    recent_activity = []
    for d in detections[:5]:
        severity = "Unknown"
        crop_name = "Unknown"
        if d.details and "analysis" in d.details and "crop_info" in d.details["analysis"]:
             crop_name = d.details["analysis"]["crop_info"].get("name", "Unknown")
        
        recent_activity.append({
            "id": str(d.id),
            "crop": crop_name,
            "disease": d.detected_disease,
            "severity": severity,
            "date": d.created_at.isoformat()
        })
        
    # Chart Data: Scans per day (last 7 days)
    chart_data = []
    today = datetime.utcnow().date()
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        day_str = date.strftime("%Y-%m-%d")
        
        # Count for this day
        count = 0
        for d in detections:
            if d.created_at.date() == date:
                count += 1
        
        chart_data.append({
            "name": date.strftime("%a"), # Mon, Tue
            "scans": count
        })

    return {
        "total_scans": total_scans,
        "diseases_found": diseases_count,
        "crops_monitored": crops_count,
        "health_score": health_score,
        "recent_activity": recent_activity,
        "chart_data": chart_data
    }

@router.get("/{id}", response_model=Any)
def get_report_detail(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get detailed information for a specific crop report.
    """
    print(f"DEBUG: Fetching report {id} for user {current_user.email} (ID: {current_user.id})")
    detection = db.query(DiseaseDetection).filter(
        DiseaseDetection.id == id,
        DiseaseDetection.user_id == current_user.id
    ).first()
    
    if not detection:
        print(f"DEBUG: Report {id} not found for user {current_user.id}")
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Report {id} not found for current user")
        
    from fastapi.encoders import jsonable_encoder
    return jsonable_encoder(detection)
