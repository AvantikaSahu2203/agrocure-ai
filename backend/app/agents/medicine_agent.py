from typing import Any, Dict
from .base import BaseAgent
from app.services.medicine_service import medicine_service

class MedicineRecommendationAgent(BaseAgent):
    """
    Agent responsible for recommending treatments.
    Uses centralized MedicineRecommendationService with high-quality disease data.
    """
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data: {
                "disease_name": str,
                "crop_name": str
            }
        """
        disease_name = input_data.get("disease_name", "Unknown")
        crop_name = input_data.get("crop_name", "")
        
        # Use centralized service with crop context for high precision
        med_info = medicine_service.get_recommendation(disease_name, crop_name)
        
        # Extract fields from our rich database result
        chemical_name = med_info.get("chemical_medicine", "Broad-spectrum Fungicide")
        organic_name = med_info.get("organic_remedy", "Neem Oil Spray")
        dosage = med_info.get("dosage", "2g/L for powders, 2ml/L for liquids")
        
        # Handle lists or strings for recommendations
        base_preventative = [
            "Rotate crops every season",
            "Ensure balanced soil nutrition (N-P-K)",
            "Space plants for proper air movement",
            "Remove and burn infected leaves early"
        ]
        
        db_recs = med_info.get("recommendations", [])
        if isinstance(db_recs, list) and len(db_recs) > 0:
            preventative_measures = db_recs + base_preventative
        else:
            preventative_measures = base_preventative

        # Limit to unique measures
        preventative_measures = list(dict.fromkeys(preventative_measures))[:5]

        # Handle Healthy case
        application_method = "Foliar Spray"
        frequency = "Once every 7-10 days until symptoms subside"
        
        if "Healthy" in disease_name or "None" in chemical_name:
            application_method = "Standard Maintenance"
            frequency = "As per seasonal schedule"
            if "Healthy" in disease_name:
                dosage = "N/A"

        return {
            "chemical_treatments": [chemical_name],
            "organic_treatments": [organic_name],
            "dosage": dosage,
            "application_method": application_method,
            "frequency": frequency,
            "preventative_measures": preventative_measures
        }
