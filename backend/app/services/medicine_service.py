import json
import os
from typing import Dict, List, Optional
from app.data.disease_data import DISEASE_DATABASE

class MedicineRecommendationService:
    """
    Service for providing specific medicine recommendations based on disease.
    """
    def __init__(self, db_path: str = "app/data/medicine_db.json"):
        self.db_path = db_path
        self.database = self._load_database()

    def _load_database(self) -> List[Dict]:
        """Loads the medicine database from JSON."""
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return []

    def get_recommendation(self, disease_name: str, crop_name: Optional[str] = None) -> Dict:
        """
        Lookup recommendation for a specific disease.
        Prioritizes the rich DISEASE_DATABASE if crop_name is provided.
        """
        disease_lower = disease_name.lower()
        crop_lower = crop_name.lower() if crop_name else None

        # Handle Healthy case explicitly
        if "healthy" in disease_lower:
            return {
                "disease": "Healthy",
                "chemical_medicine": "None",
                "organic_remedy": "None",
                "dosage": "N/A",
                "recommendations": ["Maintain standard care"]
            }

        # 1. Try Rich DISEASE_DATABASE Search (High Precision)
        if crop_lower and crop_lower in DISEASE_DATABASE:
            for d_info in DISEASE_DATABASE[crop_lower]:
                if d_info["name"].lower() in disease_lower or disease_lower in d_info["name"].lower():
                    return {
                        "disease": d_info["name"],
                        "chemical_medicine": d_info.get("chemical_treatment", "Consult expert"),
                        "organic_remedy": d_info.get("organic_treatment", "Neem Oil"),
                        "dosage": d_info.get("dosage", "As per label"),
                        "recommendations": d_info.get("recommendations", [])
                    }

        # 2. Try Global Search in DISEASE_DATABASE (Across all crops)
        for crop, diseases in DISEASE_DATABASE.items():
            for d_info in diseases:
                if d_info["name"].lower() == disease_lower:
                    return {
                        "disease": d_info["name"],
                        "chemical_medicine": d_info.get("chemical_treatment", "Consult expert"),
                        "organic_remedy": d_info.get("organic_treatment", "Neem Oil"),
                        "dosage": d_info.get("dosage", "As per label"),
                        "recommendations": d_info.get("recommendations", [])
                    }

        # 3. Fallback to JSON database
        for entry in self.database:
            if entry["disease"].lower() in disease_lower or disease_lower in entry["disease"].lower():
                return entry
                
        # 4. Final Fallback
        return {
            "disease": disease_name,
            "chemical_medicine": "Broad-spectrum fungicide (e.g. Mancozeb)",
            "organic_remedy": "Neem Oil Spray (5ml/L)",
            "dosage": "As per product label",
            "recommendations": ["Consult local agricultural extension for specific dosage"]
        }

    def get_all_medicines(self) -> List[Dict]:
        """Returns the entire database."""
        return self.database

# Singleton instance
medicine_service = MedicineRecommendationService()
