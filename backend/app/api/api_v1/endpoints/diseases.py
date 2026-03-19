from typing import Any, List, Dict
from fastapi import APIRouter
from app.services.ai_analyzer import DISEASE_DATABASE

router = APIRouter()

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_diseases() -> Any:
    """
    Get all diseases in the library.
    """
    all_diseases = []
    
    for crop, diseases in DISEASE_DATABASE.items():
        for disease in diseases:
            # Flatten the structure
            disease_entry = disease.copy()
            disease_entry["crop_name"] = crop.capitalize()
            # Add a mock image url or icon logic if needed, frontend can handle it based on crop
            all_diseases.append(disease_entry)
            
    return all_diseases
