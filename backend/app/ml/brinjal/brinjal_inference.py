import time
import os
import numpy as np
import cv2
from datetime import datetime
import keras
import tensorflow as tf

class BrinjalInference:
    """
    Independent Brinjal Disease Detection Pipeline.
    Uses a re-baked clean model: brinjal_user_clean.keras
    Architecture defined in-code to avoid Keras 3 deserialization bugs.
    """
    def __init__(self):
        # Use the clean re-baked model (avoids Keras 3 dense-layer deserialization bug)
        # Prioritize the user-trained model (Look in root or local folder)
        self.model_path = os.path.join(os.getcwd(), "brinjal_disease_model_user.keras")
        
        # Fallback to internal app path if not found in root
        if not os.path.exists(self.model_path):
             self.model_path = os.path.join(os.path.dirname(__file__), "brinjal_disease_model_user.keras")
        
        # Fallback to clean or original
        if not os.path.exists(self.model_path):
            self.model_path = os.path.join(os.path.dirname(__file__), "brinjal_user_clean.keras")
        if not os.path.exists(self.model_path):
            self.model_path = os.path.join(os.path.dirname(__file__), "brinjal_disease_model_user.keras")
        self.model = None
        
        # EXACT class names and sequence from Untitled21 (1).ipynb (Cell 40)
        self.class_names = [
            "anthracnose",
            "bacterial_wilt",
            "brinjal_healthy",
            "little_leaf",
            "phomopsis_blight",
            "powdery_mildew",
            "verticillium_wilt"
        ]
        
        # Knowledge base for Brinjal diseases (Updated with user's supported classes)
        self.disease_details = {
            "anthracnose": {
                "scientific_name": "Colletotrichum gleosporioides",
                "symptoms": ["Sunken, circular spots on fruit", "Darkening lesions", "Premature fruit drop"],
                "recommendations": ["Apply Mancozeb", "Improve air circulation", "Remove infected fruits"]
            },
            "bacterial_wilt": {
                "scientific_name": "Ralstonia solanacearum",
                "symptoms": ["Sudden wilting of top leaves", "Browning of vascular tissues", "Stunted growth"],
                "recommendations": ["Ensure proper drainage", "Rotate with non-solanaceous crops", "Use resistant varieties"]
            },
            "brinjal_healthy": {
                "scientific_name": "N/A",
                "symptoms": ["Green, vibrant leaves", "No visible lesions"],
                "recommendations": ["Continue regular maintenance", "Apply balanced NPK fertilizer"]
            },
            "little_leaf": {
                "scientific_name": "Phytoplasma",
                "symptoms": ["Extremely small leaves", "Bushy appearance", "Short internodes"],
                "recommendations": ["Remove and burn infected plants", "Control leafhopper vectors", "Avoid keeping old plants"]
            },
            "phomopsis_blight": {
                "scientific_name": "Phomopsis vexans",
                "symptoms": ["Circular brown spots on leaves", "Stem cankers", "Fruit rot with pycnidia"],
                "recommendations": ["Treat seeds with fungicides", "Improve plant spacing", "Remove affected plant parts"]
            },
            "powdery_mildew": {
                "scientific_name": "Leveillula taurica",
                "symptoms": ["White powdery coating on leaves", "Yellowing of leaf tissue", "Downward curling of leaves"],
                "recommendations": ["Apply Sulfur-based fungicides", "Reduce leaf moisture", "Remove heavily infected lower leaves"]
            },
            "verticillium_wilt": {
                "scientific_name": "Verticillium dahliae",
                "symptoms": ["Yellowing of lower leaves", "Wilting during the day", "Brown discoloration inside the stem"],
                "recommendations": ["Crop rotation with non-host crops", "Ensure soil drainage", "Remove infected debris"]
            }
        }

    def _build_architecture(self):
        """Rebuild the exact architecture from train_user_brinjal.py"""
        inputs = keras.Input(shape=(224, 224, 3))
        base_model = keras.applications.MobileNetV2(
            input_shape=(224, 224, 3),
            include_top=False,
            weights=None
        )
        base_model.trainable = True
        
        x = base_model(inputs)
        x = keras.layers.GlobalAveragePooling2D()(x)
        x = keras.layers.Dense(128, activation='relu')(x)
        x = keras.layers.Dropout(0.5)(x)
        outputs = keras.layers.Dense(7, activation='softmax')(x)
        
        model = keras.Model(inputs, outputs)
        return model

    def _load_model(self):
        if self.model is not None:
            return True
        try:
            # Keras 3 direct loading for .keras files
            if os.path.exists(self.model_path):
                self.model = keras.models.load_model(self.model_path, compile=False)
                print(f"[BrinjalInference] Keras 3 model loaded from {self.model_path}")
                return True
            else:
                # Fallback to the other path if user-specific model is not found
                original_path = os.path.join(os.path.dirname(__file__), "brinjal_disease_model_user.keras")
                if os.path.exists(original_path):
                    self.model = keras.models.load_model(original_path, compile=False)
                    print(f"[BrinjalInference] Standard model loaded from {original_path}")
                    return True
                return False
        except Exception as e:
            print(f"[BrinjalInference] Failed to load model: {e}")
            # Final fallback: Rebuild architecture and try loading weights
            try:
                print("[BrinjalInference] Attempting manual architecture reconstruction...")
                self.model = self._build_architecture()
                if os.path.exists(self.model_path):
                     self.model.load_weights(self.model_path)
                return True
            except Exception as e2:
                print(f"[BrinjalInference] Manual reconstruction also failed: {e2}")
        return False


    def predict(self, image_bytes: bytes):
        """
        Runs independent inference using the user's perfect model logic.
        """
        if not self._load_model():
            return self._mock_predict()

        try:
            # 2. Pre-process Image
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (224, 224))
            
            # STICKING TO USER STEPS: [0, 1] Normalization (Untitled21 (1).ipynb Cell 33/40)
            img_array = img.astype(np.float32) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # 3. Inference
            preds = self.model.predict(img_array, verbose=0)
            class_idx = np.argmax(preds[0])
            confidence = float(preds[0][class_idx])
            
            # Debug: Log all probabilities
            prob_map = {name: float(preds[0][i]) for i, name in enumerate(self.class_names)}
            print(f"--- USER MODEL PREDICTION ---")
            print(f"Winner: {self.class_names[class_idx]} ({confidence:.2f})")
            
            disease_name = self.class_names[class_idx]
            
            # 4. Enrich with Details
            details = self.disease_details.get(disease_name, {})
            
            return {
                "disease_name": disease_name.replace("_", " ").title(), # Format for UI
                "scientific_name": details.get("scientific_name", "Solanum melongena pathogen"),
                "confidence": float(round(confidence, 2)),
                "all_probabilities": prob_map,
                "symptoms": details.get("symptoms", []),
                "tips": details.get("recommendations", []),
                "severity": "High" if confidence > 0.8 else "Medium",
                "is_brinjal_specialized": True
            }
        except Exception as e:
            print(f"User Model Inference Error: {e}")
            return self._mock_predict()

    def _mock_predict(self):
        return {
            "disease_name": "Model Error",
            "scientific_name": "N/A",
            "confidence": 0.0,
            "symptoms": ["Could not load user's brinjal model"],
            "tips": ["Ensure 'brinjal_disease_model_user.keras' exists in the backend"],
            "severity": "Unknown",
            "is_brinjal_specialized": True,
            "error": "Model loading failed"
        }
