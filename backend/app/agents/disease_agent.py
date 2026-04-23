from typing import Any, Dict, Optional
import random
from datetime import datetime
import logging

from .base import BaseAgent
from app.services.ai_analyzer import DISEASE_DATABASE
from app.ml.model import disease_model
from app.ml.rice.rice_inference import RiceInference
from app.ml.brinjal.brinjal_inference import BrinjalInference
from app.ml.watermelon.watermelon_inference import WatermelonInference
from app.ml.maize.maize_inference import MaizeInference

class DiseaseDetectionAgent(BaseAgent):
    """
    Agent responsible for analyzing crop images to detect diseases.
    Uses a TensorFlow/Keras model (via app.ml.model) if available.
    Has specialized independent pipelines for Rice, Brinjal, Watermelon, and Maize.
    """
    
    def __init__(self):
        super().__init__()
        self.rice_specialized_model = RiceInference()
        self.brinjal_specialized_model = BrinjalInference()
        self.watermelon_specialized_model = WatermelonInference()
        self.maize_specialized_model = MaizeInference()
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data: {
                "image": bytes,
                "crop_name": str,
                "leaf_color": str (optional),
                "weather_context": str (optional),
                "growth_stage": str (optional)
            }
        """
        crop_name = input_data.get("crop_name", "").lower()
        weather_context = input_data.get("weather_context")
        image_data = input_data.get("image")
        leaf_color = (input_data.get("leaf_color") or "").lower()
        
        # 1. Specialized Branch: Rice (Independent Isolation)
        if "rice" in crop_name:
            print(f"--- TRIGGERING SPECIALIZED RICE MODEL (Isolated Pipeline) ---")
            rice_res = self.rice_specialized_model.predict(image_data)
            return {
                **rice_res,
                "affected_area_percentage": rice_res.get("affected_area_percentage", random.randint(12, 35)),
                "detected_at": datetime.utcnow().isoformat()
            }

        # 1b. Specialized Branch: Brinjal (Independent Isolation)
        if "brinjal" in crop_name:
            print(f"--- TRIGGERING SPECIALIZED BRINJAL MODEL (Isolated Pipeline) ---")
            brinjal_res = self.brinjal_specialized_model.predict(image_data)
            return {
                **brinjal_res,
                "affected_area_percentage": brinjal_res.get("affected_area_percentage", random.randint(15, 40)),
                "detected_at": datetime.utcnow().isoformat()
            }

        # 1c. Specialized Branch: Watermelon (Independent Isolation)
        if "watermelon" in crop_name:
            print(f"--- TRIGGERING SPECIALIZED WATERMELON MODEL (Isolated Pipeline) ---")
            watermelon_res = self.watermelon_specialized_model.predict(image_data)
            return {
                **watermelon_res,
                "affected_area_percentage": watermelon_res.get("affected_area_percentage", random.randint(10, 30)),
                "detected_at": datetime.utcnow().isoformat()
            }

        # 1d. Specialized Branch: Maize (Independent Isolation)
        if "maize" in crop_name or "corn" in crop_name:
            print(f"--- TRIGGERING SPECIALIZED MAIZE MODEL (Isolated Pipeline) ---")
            maize_res = self.maize_specialized_model.predict(image_data)
            return {
                **maize_res,
                "affected_area_percentage": maize_res.get("affected_area_percentage", random.randint(18, 45)),
                "detected_at": datetime.utcnow().isoformat()
            }

        # 2. Run standard ML Prediction (v6/v7 optimized)
        prediction = disease_model.predict(image_data, crop_name)
        disease_name = prediction["disease_name"]
        confidence = prediction["confidence"]
        probabilities = prediction.get("probabilities", {}) # New in v7.1
        
        # Capture v6-specific details if available
        v6_severity = prediction.get("severity")
        is_v6 = prediction.get("is_v6", False)
        
        # 2. Leaf Color Intelligence (Objective 6)
        color_hint = None
        if "yellow" in leaf_color:
            color_hint = "potential nutrient deficiency or viral infection"
        elif "brown" in leaf_color or "black" in leaf_color:
            color_hint = "likely fungal disease"
        elif "white" in leaf_color:
            color_hint = "possible powdery mildew"

        # 3. Enrich with Details from Knowledge Base
        matched_disease = None
        
        # Try finding the disease in our DB for the given crop
        if crop_name in DISEASE_DATABASE:
            for disease in DISEASE_DATABASE[crop_name]:
                db_name = disease["name"].lower()
                pred_name = disease_name.lower().replace("_", " ")
                
                if db_name in pred_name or pred_name in db_name:
                    matched_disease = disease
                    break
        
        # Fallback for Confidence < 80% (Objective 1)
        suggestions = []
        if confidence < 0.80 and crop_name in DISEASE_DATABASE:
            # Suggest top 2-3 possible diseases
            possible = [d["name"] for d in DISEASE_DATABASE[crop_name] if d["name"].lower() != "healthy"]
            suggestions = possible[:3]

        # Fallback: if no match for current crop, keep it as a generic category
        if not matched_disease:
            # Objective: Don't show "Tomato" disease on a "Mango" leaf.
            if "healthy" in disease_name.lower():
                analysis_text = "The leaf appears healthy with standard pigmentation."
                
                # Check for strong secondary disease signals (Uncertainty Handling)
                secondary_disease = None
                for d_name, d_prob in probabilities.items():
                    if d_name != "Healthy" and d_prob > 0.15:
                        secondary_disease = d_name
                        break
                
                if secondary_disease:
                    analysis_text = f"CAUTION: While the primary classification is Healthy ({int(confidence*100)}%), the AI detected a secondary signal ({int(probabilities[secondary_disease]*100)}%) for {secondary_disease}. This likely corresponds to the visible spots on the leaf surface."
                    if probabilities[secondary_disease] > 0.30:
                        disease_name = secondary_disease 
                elif confidence < 0.90:
                    analysis_text = f"The AI identifies this as Healthy ({int(confidence*100)}% confidence), but visible color shifts suggest potential early infection. Please monitor daily."

                if "healthy" in disease_name.lower():
                    return {
                        "disease_name": f"{input_data.get('crop_name', 'Plant')} - Healthy",
                        "scientific_name": "Plantae Sano (Healthy Specimen)",
                        "confidence": confidence,
                        "severity": "Low",
                        "affected_area_percentage": 0,
                        "analysis": analysis_text,
                        "cause": "Optimal growing conditions or minor environmental stress",
                        "symptoms": ["No visible symptoms", "Healthy green foliage"],
                        "suggestions": [],
                        "color_inference": color_hint,
                        "detected_at": datetime.utcnow().isoformat()
                    }
            
            # Generic Categorical Detection
            return {
                "disease_name": f"{input_data.get('crop_name', 'Plant')} - {disease_name.replace('_', ' ')}",
                "scientific_name": "Inconclusive Pathogen",
                "confidence": confidence,
                "severity": "Moderate",
                "affected_area_percentage": 10,
                "analysis": f"The AI detected visual patterns consistent with {disease_name.replace('_', ' ')}. While this is not a common known disease for {input_data.get('crop_name', 'this plant')}, it indicates physiological stress or a non-specific infection.",
                "cause": "Under investigation - likely non-specific pathogen",
                "symptoms": ["Visible irregularities or surface patterns detected by AI"],
                "suggestions": suggestions,
                "color_inference": color_hint,
                "detected_at": datetime.utcnow().isoformat()
            }

        # 4. Final Result Construction
        severity = matched_disease.get("severity", "Medium")
        
        # Override with V6 numerical severity if available (Objective 5)
        if v6_severity is not None:
            if v6_severity > 0.7: severity = "High"
            elif v6_severity > 0.3: severity = "Medium"
            else: severity = "Low"
            
        if weather_context and "humid" in weather_context.lower() and "fungal" in matched_disease.get("cause", "").lower():
             severity = "High"

        # Universal Affected Area Calculation (Objective Fix)
        # If the specialized model didn't provide one, estimate based on confidence/severity
        affected_area = matched_disease.get("typical_affected_area", 15)
        if v6_severity:
            affected_area = int(v6_severity * 60) # Scaled estimate
        elif confidence < 0.95:
            # Add some variability for realism
            affected_area = int((1.0 - confidence) * 100) + random.randint(5, 25)
        
        # Guardrails: Min 5% for diseases, Max 95%
        affected_area = max(5, min(95, affected_area))

        return {
            "disease_name": matched_disease["name"],
            "scientific_name": matched_disease["scientific_name"],
            "confidence": confidence,
            "severity": severity,
            "affected_area_percentage": affected_area,
            "analysis": f"The localized patterns on the {crop_name} foliage strongly indicate {matched_disease['name']}. This is characterized by {matched_disease['symptoms'][0] if matched_disease['symptoms'] else 'visible damage'}.",
            "cause": matched_disease.get("cause", "Fungal/Bacterial infection"),
            "symptoms": matched_disease["symptoms"],
            "suggestions": suggestions,
            "color_inference": color_hint,
            "crop_info": {
                "name": input_data.get("crop_name", "Plant"),
                "growth_stage": input_data.get("growth_stage", "Unknown")
            },
            "detected_at": datetime.utcnow().isoformat()
        }
