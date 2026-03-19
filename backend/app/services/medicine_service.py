import json
import os
from typing import Dict, List, Optional

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

    def get_recommendation(self, disease_name: str) -> Dict:
        """
        Lookup recommendation for a specific disease.
        Supports fuzzy matching (contains).
        """
        disease_lower = disease_name.lower()
        
        # Try exact/substring match
        for entry in self.database:
            if entry["disease"].lower() in disease_lower or disease_lower in entry["disease"].lower():
                return entry
                
        # Fallback if no specific match
        return {
            "disease": disease_name,
            "chemical_medicine": "Broad-spectrum fungicide/pesticide (Consult local expert)",
            "organic_remedy": "Neem Oil Spray (5ml/L) or Garlic extract"
        }

    def get_all_medicines(self) -> List[Dict]:
        """Returns the entire database."""
        return self.database

# Singleton instance
medicine_service = MedicineRecommendationService()
