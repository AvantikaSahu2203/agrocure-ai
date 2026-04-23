import os
import numpy as np
from PIL import Image
import io
import logging

import keras
import tensorflow as tf
logging.basicConfig(level=logging.INFO)

try:
    from .v6.agri_ai.inference_v6 import AgriInferenceV6
except ImportError:
    AgriInferenceV6 = None

try:
    from .v7.inference_v7 import AgriInferenceV7
except Exception as e:
    import traceback
    print(f"DEBUG: AgriInferenceV7 Import Failed!")
    print(traceback.format_exc())
    AgriInferenceV7 = None

# Direct independent imports
try:
    from .brinjal.brinjal_inference import BrinjalInference
except ImportError:
    BrinjalInference = None

try:
    from .rice.rice_inference import RiceInference
except ImportError:
    RiceInference = None

try:
    from .watermelon.watermelon_inference import WatermelonInference
except ImportError:
    WatermelonInference = None

class DiseaseModel:
    def __init__(self, model_path: str = "app/ml/plant_disease_model.h5"):
        self.model_path = model_path
        self.v6_weights = "app/ml/v6/agri_ai/model/weights/agrinet_x_v1.pt"
        self.v7_weights = "app/ml/v7/plant_disease_prediction_model.h5"
        self.model = None
        self.v6_engine = None
        self.v7_engine = None
        self.brinjal_engine = None
        self.rice_engine = None
        self.watermelon_engine = None
        self.is_loaded = False
        
        # 0. Attempt V7 (Keras 38-class) Initialization
        if AgriInferenceV7 and os.path.exists(self.v7_weights):
            try:
                # v7 now points to the new Keras engine
                self.v7_engine = AgriInferenceV7(self.v7_weights)
                self.is_loaded = True
                logging.info("AgroCure AI Keras v7.1 (38-class) initialized.")
            except Exception as e:
                print(f"DEBUG: v7 initialization catch: {e}")
                logging.error(f"Failed to load V7 Keras engine: {e}")

        if BrinjalInference:
            self.brinjal_engine = BrinjalInference()
            
        if RiceInference:
            self.rice_engine = RiceInference()

        if WatermelonInference:
            self.watermelon_engine = WatermelonInference()

        # ... (rest of the init remains same)
        
        self.class_names = [
            "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
            "Blueberry___healthy", "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy",
            "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Corn_(maize)___Common_rust_",
            "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy",
            "Grape___Black_rot", "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
            "Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot", "Peach___healthy",
            "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy",
            "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
            "Raspberry___healthy", "Soybean___healthy", "Squash___Powdery_mildew",
            "Strawberry___Leaf_scorch", "Strawberry___healthy",
            "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight",
            "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot",
            "Tomato___Spider_mites Two-spotted_spider_mite", "Tomato___Target_Spot",
            "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus", "Tomato___healthy"
        ]

    def _load_legacy_model(self):
        """Loads the model from disk if available."""
        if os.path.exists(self.model_path):
            try:
                self.model = keras.models.load_model(self.model_path)
                self.is_loaded = True
                logging.info(f"ML Model loaded from {self.model_path}")
            except Exception as e:
                logging.error(f"Failed to load ML model: {e}")
        else:
            logging.warning(f"ML Model not found at {self.model_path}. Using Mock Mode.")

    def preprocess_image(self, image_bytes: bytes, target_size=(224, 224)) -> np.ndarray:
        """
        Converts bytes to PIL Image, resizes, and normalizes.
        Returns batch format: (1, 224, 224, 3)
        """
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != "RGB":
            image = image.convert("RGB")
        image = image.resize(target_size)
        image_array = np.array(image)
        image_array = image_array / 255.0  # Normalize to [0, 1]
        image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
        return image_array

    def predict(self, image_bytes: bytes, crop_name: str = None):
        """
        Runs prediction on the image. Prioritizes Independent Models -> V7 (Ensemble) -> V6 -> Legacy -> Mock.
        """
        crop_lower = crop_name.lower() if crop_name else ""

        # Prioritize Independent Specialized Models
        if "brinjal" in crop_lower and self.brinjal_engine:
            try:
                res = self.brinjal_engine.predict(image_bytes)
                return {
                    "disease_name": res["disease_name"],
                    "confidence": res["confidence"],
                    "severity": res.get("severity", 0.8),
                    "is_specialized": True
                }
            except Exception as e:
                logging.error(f"Brinjal Prediction error: {e}")

        if "rice" in crop_lower and self.rice_engine:
            try:
                res = self.rice_engine.predict(image_bytes)
                return {
                    "disease_name": res["disease_name"],
                    "confidence": res["confidence"],
                    "severity": res.get("severity", 0.8),
                    "is_specialized": True
                }
            except Exception as e:
                logging.error(f"Rice Prediction error: {e}")

        if "watermelon" in crop_lower and self.watermelon_engine:
            try:
                res = self.watermelon_engine.predict(image_bytes)
                return {
                    "disease_name": res["disease_name"],
                    "confidence": res["confidence"],
                    "severity": res.get("severity", 0.8),
                    "is_specialized": True
                }
            except Exception as e:
                logging.error(f"Watermelon Prediction error: {e}")

        # 3. V7 Ensemble (Fallback only for standard PlantVillage crops)
        plant_village_crops = ["apple", "cherry", "corn", "grape", "orange", "peach", "pepper", "potato", "raspberry", "soybean", "squash", "strawberry", "tomato"]
        
        is_pv_crop = any(pv in crop_lower for pv in plant_village_crops)
        
        if self.v7_engine and (not crop_name or is_pv_crop):
            try:
                res = self.v7_engine.predict(image_bytes, crop_name)
                return {
                    "disease_name": res["disease_name"],
                    "confidence": res["confidence"],
                    "probabilities": res.get("probabilities", {}),
                    "severity": res.get("severity", 0.5),
                    "is_v7": True
                }
            except Exception as e:
                logging.error(f"V7 Prediction error: {e}")

        # 4. Strict Refusal for Unsupported Specialized Crops
        if crop_name and not is_pv_crop:
             return {
                "disease_name": f"Inconclusive ({crop_name} Specialized Model Offline)",
                "confidence": 0.0,
                "analysis": f"The AI cannot accurately diagnose {crop_name} using the generic model. Please ensure the specialized {crop_name} model is active.",
                "is_uncertain": True
            }

        return self._mock_predict(crop_name)

    def _mock_predict(self, crop_name: str):
        """
        Fallback mock prediction if model is missing.
        Uses a random selection from likely diseases for the crop.
        """
        import random
        from app.services.ai_analyzer import DISEASE_DATABASE
        
        # Default fallback
        disease_name = "Healthy"
        confidence = round(random.uniform(0.7, 0.99), 2)
        
        if crop_name:
            crop_lower = crop_name.lower()
            if crop_lower in DISEASE_DATABASE:
                diseases = DISEASE_DATABASE[crop_lower]
                if diseases:
                    # Pick a random disease or healthy
                    # 20% chance of healthy if available, else random disease
                    if random.random() < 0.2:
                         disease_name = f"{crop_name} Healthy"
                    else:
                         selected = random.choice(diseases)
                         disease_name = selected["name"]
        
        return {
            "disease_name": disease_name,
            "confidence": confidence,
            "is_mock": True
        }

# Global instance
disease_model = DiseaseModel()
