import os
import joblib
import numpy as np
from typing import Dict, List, Optional

class SoilAnalysisService:
    """
    Predicts nutrient deficiencies and soil-related diseases based on soil parameters.
    """
    DEFICIENCIES = ["Nitrogen", "Phosphorus", "Potassium", "Iron", "Magnesium"]
    SOIL_DISEASES = ["Root Rot", "Fusarium Wilt", "Damping Off", "Clubroot"]

    def __init__(self, model_path: str = "app/ml/v4/soil_model_lgbm.joblib"):
        self.model_path = model_path
        self.model = self._load_model()

    def _load_model(self):
        """Loads the pre-trained LightGBM model."""
        if os.path.exists(self.model_path):
            try:
                return joblib.load(self.model_path)
            except Exception as e:
                print(f"Error loading soil model: {e}")
        return None

    def analyze_soil(self, ph: float, n: float, p: float, k: float) -> Dict:
        """Analyze soil parameters for deficiencies and diseases."""
        # Feature vector: [pH, N, P, K]
        X = np.array([[ph, n, p, k]])

        if self.model:
            # Multi-output prediction
            prediction = self.model.predict(X)[0]
            # Assuming the model outputs 1 for presence and 0 for absence
            # Index 0-4: Deficiencies, Index 5-8: Diseases
            deficiencies = [self.DEFICIENCIES[i] for i in range(len(self.DEFICIENCIES)) if prediction[i] > 0.5]
            diseases = [self.SOIL_DISEASES[i] for i in range(len(self.SOIL_DISEASES)) if prediction[i+len(self.DEFICIENCIES)] > 0.5]
        else:
            # Fallback to heuristic logic
            deficiencies, diseases = self._heuristic_analysis(ph, n, p, k)

        return {
            "deficiencies": deficiencies,
            "soil_diseases": diseases,
            "parameters": {
                "ph": ph,
                "nitrogen": n,
                "phosphorus": p,
                "potassium": k
            },
            "risk_level": "High" if diseases else ("Moderate" if deficiencies else "Low")
        }

    def _heuristic_analysis(self, ph: float, n: float, p: float, k: float) -> (List[str], List[str]):
        """Heuristic calculation for soil analysis if ML model is unavailable."""
        deficiencies = []
        diseases = []

        # Nutrient thresholds (generic)
        if n < 30: deficiencies.append("Nitrogen")
        if p < 15: deficiencies.append("Phosphorus")
        if k < 20: deficiencies.append("Potassium")
        
        # pH related
        if ph < 5.5: deficiencies.append("Magnesium")
        if ph > 7.5: deficiencies.append("Iron")

        # Disease probability based on pH and poor drainage (represented by extreme parameters)
        if ph < 5.0: diseases.append("Clubroot")
        if ph > 6.5 and n > 100: diseases.append("Fusarium Wilt")

        return deficiencies, diseases

if __name__ == "__main__":
    # Test
    service = SoilAnalysisService()
    print(service.analyze_soil(6.2, 25.0, 10.0, 18.0))
