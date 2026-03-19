import os
import numpy as np
from PIL import Image
import io
import logging

# Try importing tensorflow, but handle failure gracefully if installation issues occur
try:
    import tensorflow as tf
except ImportError:
    tf = None

try:
    from .v6.agri_ai.inference_v6 import AgriInferenceV6
except ImportError:
    AgriInferenceV6 = None

class DiseaseModel:
    def __init__(self, model_path: str = "app/ml/plant_disease_model.h5"):
        self.model_path = model_path
        self.v6_weights = "app/ml/v6/agri_ai/model/weights/agrinet_x_v1.pt"
        self.model = None
        self.v6_engine = None
        self.is_loaded = False
        
        # 1. Attempt V6 (SOTA) Initialization
        if AgriInferenceV6 and os.path.exists(self.v6_weights):
            try:
                self.v6_engine = AgriInferenceV6(self.v6_weights)
                self.is_loaded = True
                logging.info("AgriNet-X v6 (Swin-V2) initialized.")
            except Exception as e:
                logging.error(f"Failed to load V6 engine: {e}")
                
        # 2. Fallback to Legacy TF model if V6 failed
        if not self.is_loaded:
             self._load_legacy_model()
             
        self.class_names = [
            "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
            "Blueberry___healthy",
            "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy",
            "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Corn_(maize)___Common_rust_", "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy",
            "Grape___Black_rot", "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
            "Orange___Haunglongbing_(Citrus_greening)",
            "Peach___Bacterial_spot", "Peach___healthy",
            "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy",
            "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
            "Raspberry___healthy",
            "Soybean___healthy",
            "Squash___Powdery_mildew",
            "Strawberry___Leaf_scorch", "Strawberry___healthy",
            "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite", "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus", "Tomato___healthy"
        ]

    def _load_legacy_model(self):
        """Loads the model from disk if available."""
        if tf and os.path.exists(self.model_path):
            try:
                self.model = tf.keras.models.load_model(self.model_path)
                self.is_loaded = True
                logging.info(f"ML Model loaded from {self.model_path}")
            except Exception as e:
                logging.error(f"Failed to load ML model: {e}")
        else:
            logging.warning(f"ML Model not found at {self.model_path} or TensorFlow not installed. Using Mock Mode.")

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
        Runs prediction on the image. Prioritizes V6 (SOTA) -> Legacy -> Mock.
        """
        # Prioritize V6 Engine (Two-Stage Swin-V2)
        if self.v6_engine:
            try:
                res = self.v6_engine.predict(image_bytes, crop_name)
                # Map v6 format to expected orchestrator format
                return {
                    "disease_name": res["disease_name"],
                    "confidence": res["confidence"],
                    "severity": res.get("severity", 0.5),
                    "is_v6": True
                }
            except Exception as e:
                logging.error(f"V6 Prediction error: {e}")

        # Legacy TensorFlow Path
        if self.is_loaded and self.model:
            try:
                processed_image = self.preprocess_image(image_bytes)
                predictions = self.model.predict(processed_image)
                predicted_index = np.argmax(predictions[0])
                confidence = float(np.max(predictions[0]))
                disease_name = self.class_names[predicted_index]
                
                return {
                    "disease_name": disease_name,
                    "confidence": confidence
                }
            except Exception as e:
                logging.error(f"Legacy Prediction error: {e}")
                return self._mock_predict(crop_name)
        else:
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
