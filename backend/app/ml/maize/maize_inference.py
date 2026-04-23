import os
import numpy as np
import cv2
from datetime import datetime
import keras
import tensorflow as tf

class MaizeInference:
    """
    Independent Maize Disease Detection Pipeline.
    Uses a high-accuracy EfficientNetB0 model.
    """
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), "maize_disease_v1.keras")
        self.model = None
        
        # EXACT class names matching the training order
        self.class_names = [
            "aspergillus_rot",
            "common_rust",
            "downy_mildew",
            "gray_leaf_spot",
            "healthy",
            "northern_leaf_blight"
        ]
        
        # Mapping to display names in DISEASE_DATABASE
        self.display_names = {
            "aspergillus_rot": "Aspergillus Rot",
            "common_rust": "Common Rust",
            "downy_mildew": "Downy Mildew",
            "gray_leaf_spot": "Gray Leaf Spot",
            "healthy": "Healthy",
            "northern_leaf_blight": "Northern Leaf Blight (TLB)"
        }

    def _load_model(self):
        if self.model is not None:
            return True
        try:
            if os.path.exists(self.model_path):
                # Using Keras 3 direct load for modern .keras format
                self.model = keras.models.load_model(self.model_path, compile=False)
                print(f"[MaizeInference] High-accuracy model loaded from {self.model_path}")
                return True
            else:
                print(f"[MaizeInference] Model not found at {self.model_path}")
        except Exception as e:
            print(f"[MaizeInference] Failed to load model: {e}")
        return False

    def predict(self, image_bytes: bytes):
        """
        Runs independent inference using the Maize EfficientNetB0 model.
        """
        if not self._load_model():
            return self._mock_predict()

        try:
            # 1. Image Pre-processing (Matching training parameters)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (224, 224))
            
            # Normalization 1/127.5 offset -1 to [-1, 1] (MobileNetV2 standard)
            img_array = (img.astype(np.float32) / 127.5) - 1.0
            img_array = np.expand_dims(img_array, axis=0)

            # 2. Inference
            preds = self.model.predict(img_array, verbose=0)
            class_idx = np.argmax(preds[0])
            confidence = float(preds[0][class_idx])
            
            internal_name = self.class_names[class_idx]
            display_name = self.display_names.get(internal_name, internal_name)
            
            print(f"--- MAIZE MODEL PREDICTION ---")
            print(f"Detected: {display_name} ({confidence:.2f})")
            
            return {
                "disease_name": display_name,
                "confidence": float(round(confidence, 2)),
                "is_maize_specialized": True,
                "status": "Success"
            }
        except Exception as e:
            print(f"Maize Model Inference Error: {e}")
            return self._mock_predict()

    def _mock_predict(self):
        return {
            "disease_name": "Maize Diagnostic Offline",
            "scientific_name": "N/A",
            "confidence": 0.0,
            "analysis": "Specialized Maize model is still being optimized or is unavailable.",
            "is_maize_specialized": True,
            "status": "Incomplete"
        }
