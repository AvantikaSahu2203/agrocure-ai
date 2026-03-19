from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class SoilData(BaseModel):
    soil_type: Optional[str] = None
    n: Optional[float] = None
    p: Optional[float] = None
    k: Optional[float] = None

class AdvisoryRequest(BaseModel):
    lat: float
    lon: float
    crop_name: str
    growth_stage: str # Seedling, Vegetative, Flowering, Harvest
    soil_data: Optional[SoilData] = None

class WeatherAdvice(BaseModel):
    summary: str
    temp: float
    humidity: float
    rain_probability: float
    actionable_steps: List[str]

class GrowthAdvice(BaseModel):
    stage: str
    fertilizer_schedule: str
    irrigation_schedule: str
    spray_schedule: str

class AdvisoryResponse(BaseModel):
    weather: WeatherAdvice
    soil_fertilizer: Dict[str, Any]
    growth_stage_timeline: GrowthAdvice
    disease_risk: Dict[str, Any]
    market_mandi: Dict[str, Any]
    voice_advice: str
    timestamp: str
