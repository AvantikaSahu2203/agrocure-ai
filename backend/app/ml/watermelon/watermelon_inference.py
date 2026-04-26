import time
import os
import numpy as np
import cv2
from datetime import datetime
import tensorflow as tf
from tensorflow import keras

class WatermelonInference:
    """
    Independent Watermelon Disease Detection Pipeline.
    Uses the trained model: watermelon_disease_v1.keras
    """
    def __init__(self):
        # Use the specific backend directory path
        self.model_path = os.path.join(os.path.dirname(__file__), "watermelon_disease_v1.keras")
        
        # Fallback to current working directory
        if not os.path.exists(self.model_path):
            self.model_path = os.path.join(os.getcwd(), "watermelon_disease_v1.keras")

        
        self.model = None
        
        # Exact class names based on download_watermelon.py logic
        self.class_names = [
            "anthracnose_leaf_spots",
            "downy_mildew_yellow_spots",
            "fusarium_wilt_symptoms",
            "leaf_healthy",
            "mosaic_virus_patterns",
            "powdery_mildew_white_powder"
        ]
        
        # Mapping to user-friendly names
        self.display_names = {
            "anthracnose_leaf_spots": "Anthracnose",
            "downy_mildew_yellow_spots": "Downy Mildew",
            "fusarium_wilt_symptoms": "Fusarium Wilt",
            "leaf_healthy": "Healthy",
            "mosaic_virus_patterns": "Mosaic Virus",
            "powdery_mildew_white_powder": "Powdery Mildew"
        }
        
        # Knowledge base for Watermelon diseases
        self.disease_details = {
            "anthracnose_leaf_spots": {
                "scientific_name": "Colletotrichum orbiculare",
                "symptoms": ["Small, water-soaked spots on leaves", "Sunken circular lesions", "Leaf yellowing"],
                "recommendations": ["Apply Mancozeb or Chlorothalonil", "Avoid overhead irrigation", "Remove infected debris"]
            },
            "downy_mildew_yellow_spots": {
                "scientific_name": "Pseudoperonospora cubensis",
                "symptoms": ["Angular yellow spots on upper leaf surface", "Purplish-gray mold underneath"],
                "recommendations": ["Apply Metalaxyl or Ridomil Gold", "Improve plant spacing", "Reduce humidity"]
            },
            "fusarium_wilt_symptoms": {
                "scientific_name": "Fusarium oxysporum f. sp. niveum",
                "symptoms": ["Sudden wilting of vines", "Browning of vascular tissue in stems", "Stunted growth"],
                "recommendations": ["Use resistant varieties", "Practice long-term crop rotation", "Soil solarization"]
            },
            "leaf_healthy": {
                "scientific_name": "Citrullus lanatus (Healthy)",
                "symptoms": ["Vibrant green foliage", "No visible lesions", "Consistent growth"],
                "recommendations": ["Continue optimal irrigation", "Regular monitoring for pests"]
            },
            "mosaic_virus_patterns": {
                "scientific_name": "Watermelon Mosaic Virus (WMV)",
                "symptoms": ["Mottled green patterns on leaves", "Distorted leaf shape", "Stunted vine growth"],
                "recommendations": ["Control aphid vectors with Neem oil", "Remove infected plants immediately", "Control silverleaf whitefly"]
            },
            "powdery_mildew_white_powder": {
                "scientific_name": "Podosphaera xanthii",
                "symptoms": ["White powdery coating on leaves and stems", "Leaves turning yellow and falling off"],
                "recommendations": ["Apply Sulfur-based fungicides", "Improve air circulation", "Grow in full sun"]
            }
        }

    def _load_model(self):
        if self.model is not None:
            return True
        try:
            if os.path.exists(self.model_path):
                # Load with compile=False to avoid dependency on custom objects/losses during inference
                self.model = keras.models.load_model(self.model_path, compile=False)
                print(f"[WatermelonInference] Dedicated model loaded from {self.model_path}")
                return True
            else:
                print(f"[WatermelonInference] Model not found at {self.model_path}")
        except Exception as e:
            print(f"[WatermelonInference] Failed to load model: {e}")
        return False

    def predict(self, image_bytes: bytes):
        """
        Runs independent inference using the specialized Watermelon model.
        """
        if not self._load_model():
            return self._mock_predict()

        try:
            # 1. Pre-process Image
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (224, 224))
            
            # Normalization consistent with MobileNetV2/AgriNet standards
            img_array = img.astype(np.float32) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # 2. Inference
            preds = self.model.predict(img_array, verbose=0)
            class_idx = np.argmax(preds[0])
            confidence = float(preds[0][class_idx])
            
            internal_class = self.class_names[class_idx]
            display_name = self.display_names.get(internal_class, internal_class.replace("_", " ").title())
            
            # Debug: Log prediction
            print(f"--- WATERMELON SPECIALIZED PREDICTION ---")
            print(f"Detected: {display_name} ({confidence:.2f})")
            
            # 3. Enrich with Details
            details = self.disease_details.get(internal_class, {})
            
            return {
                "disease_name": display_name,
                "scientific_name": details.get("scientific_name", "Citrullus lanatus Pathogen"),
                "confidence": float(round(confidence, 2)),
                "symptoms": details.get("symptoms", ["Visible irregularities detected by specialized model"]),
                "tips": details.get("recommendations", ["Consult your local agricultural extension service"]),
                "severity": "High" if confidence > 0.8 else "Medium",
                "is_specialized": True,
                "crop_type": "watermelon"
            }
        except Exception as e:
            print(f"Watermelon Model Inference Error: {e}")
            return self._mock_predict()

    def _mock_predict(self):
        return {
            "disease_name": "Healthy",
            "scientific_name": "Citrullus lanatus",
            "confidence": 0.5,
            "symptoms": ["Generic pattern detected - model bypass"],
            "tips": ["Verify lighting and image clarity"],
            "severity": "Low",
            "is_specialized": True,
            "error": "Model load failure"
        }
