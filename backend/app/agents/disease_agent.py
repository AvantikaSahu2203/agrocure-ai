from typing import Any, Dict, Optional
import random
from datetime import datetime
import logging

from .base import BaseAgent
from app.services.ai_analyzer import DISEASE_DATABASE
from app.ml.model import disease_model

class DiseaseDetectionAgent(BaseAgent):
    """
    Agent responsible for analyzing crop images to detect diseases.
    Uses a TensorFlow/Keras model (via app.ml.model) if available.
    """
    
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
        
        # 1. Run ML Prediction (v6 optimized)
        prediction = disease_model.predict(image_data, crop_name)
        disease_name = prediction["disease_name"]
        confidence = prediction["confidence"]
        
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

        # Fallback: if no match for current crop, search all crops for this disease name
        if not matched_disease:
            for crop_key, diseases in DISEASE_DATABASE.items():
                for disease in diseases:
                    db_name = disease["name"].lower()
                    pred_name = disease_name.lower().replace("_", " ")
                    if db_name in pred_name or pred_name in db_name:
                        matched_disease = disease
                        break
                if matched_disease: break

        # Fallback for "Healthy" or Unknown
        if not matched_disease:
            if "healthy" in disease_name.lower():
                return {
                    "disease_name": f"{input_data.get('crop_name', 'Plant')} - Healthy",
                    "scientific_name": "Plantae Sano",
                    "confidence": confidence,
                    "severity": "Low",
                    "cause": "Optimal growing conditions",
                    "symptoms": ["No visible symptoms", "Healthy green foliage"],
                    "suggestions": [],
                    "color_inference": color_hint,
                    "detected_at": datetime.utcnow().isoformat()
                }
            
            # Objective 10: Confidence Calibration
            status_text = "Potential Issue Detected"
            if is_v6 and prediction.get("binary_logit", 0) > 1.0:
                 status_text = "Uncertain - Possible surface abnormality or texture-based infection detected"

            return {
                "disease_name": disease_name.replace("_", " ") if disease_name else status_text,
                "scientific_name": "Unknown Pathogen",
                "confidence": confidence,
                "severity": "Moderate",
                "cause": "Under investigation",
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

        return {
            "disease_name": matched_disease["name"],
            "scientific_name": matched_disease["scientific_name"],
            "confidence": confidence,
            "severity": severity,
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
