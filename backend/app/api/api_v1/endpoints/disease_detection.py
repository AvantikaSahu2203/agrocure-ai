from typing import Optional, Any
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.services.ai_analyzer import ai_analyzer
from app.api import deps

router = APIRouter()


@router.post("/analyze")
async def analyze_disease(
    image: UploadFile = File(..., description="Crop image for disease detection"),
    crop_name: str = Form(..., description="Name of the crop"),
    region: Optional[str] = Form(None, description="Geographic region"),
    weather: Optional[str] = Form(None, description="Current weather conditions"),
    growth_stage: Optional[str] = Form(None, description="Current growth stage"),
    lat: Optional[float] = Form(None, description="Latitude"),
    lon: Optional[float] = Form(None, description="Longitude"),
    soil_ph: Optional[float] = Form(None, description="Soil pH"),
    soil_n: Optional[float] = Form(None, description="Soil Nitrogen"),
    soil_p: Optional[float] = Form(None, description="Soil Phosphorus"),
    soil_k: Optional[float] = Form(None, description="Soil Potassium"),
    language: str = Form("en", description="Language code (en, hi, mr)"),
    current_user: Any = Depends(deps.get_current_active_user)
):
    """
    Analyze crop image for disease detection.
    
    Returns structured JSON with:
    - Disease name (common and scientific)
    - Confidence score
    - Severity level
    - Detected symptoms
    - Treatment recommendations
    - Translated content based on language parameter
    """
    try:
        # Validate image file
        if not image.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image (JPEG, PNG, etc.)"
            )
        
        # Read image data
        image_data = await image.read()
        print(f"DEBUG: Received analyze request. Crop: {crop_name}, Image Size: {len(image_data)} bytes")
        
        if len(image_data) == 0:
            raise HTTPException(
                status_code=400,
                detail="Empty image file"
            )
        
        # Perform AI analysis
        result = ai_analyzer.analyze_image(
            crop_name=crop_name,
            image_data=image_data,
            region=region,
            weather=weather,
            growth_stage=growth_stage,
            lat=lat,
            lon=lon,
            soil_ph=soil_ph,
            soil_n=soil_n,
            soil_p=soil_p,
            soil_k=soil_k,
            language=language
        )
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


@router.get("/supported-crops")
async def get_supported_crops():
    """Get list of crops supported by the AI analyzer."""
    from app.services.ai_analyzer import DISEASE_DATABASE
    
    return {
        "supported_crops": list(DISEASE_DATABASE.keys()),
        "total_count": len(DISEASE_DATABASE)
    }
