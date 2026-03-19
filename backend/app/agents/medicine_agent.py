from typing import Any, Dict
from .base import BaseAgent
from app.services.medicine_service import medicine_service

class MedicineRecommendationAgent(BaseAgent):
    """
    Agent responsible for recommending treatments.
    Uses centralized MedicineRecommendationService.
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
        
        # Use centralized service
        meds = medicine_service.get_recommendation(disease_name)
        
        # Define specific dosages and methods (Objective 3)
        # In a real app, this would come from a refined DB.
        chemical_list = [meds["chemical_medicine"]]
        organic_list = [meds["organic_remedy"]]
        
        # Add a generic fallback if needed
        if "None" not in meds["chemical_medicine"] and "Consult" not in meds["chemical_medicine"]:
            if "Mancozeb" not in meds["chemical_medicine"]:
                chemical_list.append("Mancozeb (Generic Protective Fungicide)")
        
        if "Neem" not in meds["organic_remedy"]:
            organic_list.append("Neem Oil (General Organic Control)")

        dosage = "2g/L of water for powders, 2ml/L for liquids. Spray every 7-10 days."
        if "Healthy" in disease_name:
            dosage = "N/A"

        return {
            "chemical_treatments": chemical_list[:2],
            "organic_treatments": organic_list[:1],
            "dosage": dosage,
            "application_method": "Foliar Spray",
            "frequency": "Once every 7 days until symptoms subside",
            "preventative_measures": [
                "Rotate crops every season",
                "Ensure balanced soil nutrition (N-P-K)",
                "Space plants for proper air movement",
                "Remove and burn infected leaves early"
            ]
        }
