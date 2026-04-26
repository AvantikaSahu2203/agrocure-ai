import sys
import os

# Ultra-Fast Global Path Injection
GLOBAL_SITES = r"C:\Users\ASUS\AppData\Local\Programs\Python\Python310\Lib\site-packages"
if GLOBAL_SITES not in sys.path:
    sys.path.insert(0, GLOBAL_SITES)

import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import io

class AgriInferenceV7:
    """
    AgroCure AI Keras Inference v7.2
    Uses the 38-class Plant Disease CNN model (224x224).
    """
    def __init__(self, model_path: str, device: str = "cpu"):
        print(f"DEBUG: AgriInferenceV7 - Initializing with .h5 model: {model_path}")
        self.model = None
        if os.path.exists(model_path):
            try:
                self.model = tf.keras.models.load_model(model_path)
                print("DEBUG: .h5 model loaded successfully.")
            except Exception as e:
                print(f"DEBUG: .h5 model loading FAILED: {e}")
                raise
        else:
            print(f"DEBUG: Model path NOT FOUND: {model_path}")
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        # 38 Classes from plant-disease-prediction-cnn source
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

    def predict(self, image_bytes: bytes, crop_name: str = None):
        """
        Takes image bytes and returns detailed prediction using the Keras model.
        Supports crop-aware filtering to eliminate cross-crop misclassification.
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")

        # 1. Preprocess (224x224 for new model)
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img = img.resize((224, 224))
        
        # 2. Convert to Array (Normalize to [0,1])
        input_arr = np.array(img).astype(np.float32) / 255.0
        input_arr = np.expand_dims(input_arr, axis=0) # (1, 224, 224, 3)
        
        # 3. Inference
        predictions = self.model.predict(input_arr)[0] # Get probabilities for first batch
        
        # 4. Crop-Aware Filtering (Objective: Fix cross-crop errors)
        final_index = np.argmax(predictions)
        
        if crop_name and crop_name.lower() != "general":
            target = crop_name.lower()
            # Map crops to V7 supported categories
            if target == "corn": target = "maize"
            if target == "cucumber": target = "squash"
            
            # Find indices that match the requested crop
            valid_indices = [i for i, name in enumerate(self.class_names) if target in name.lower()]
            
            if valid_indices:
                # Suppress (zero out) all classes that don't belong to the selected crop
                filtered_probs = np.zeros_like(predictions)
                for idx in valid_indices:
                    filtered_probs[idx] = predictions[idx]
                
                # Re-calculate argmax from filtered set
                final_index = np.argmax(filtered_probs)
                print(f"DEBUG: V7 Filtering active for {crop_name}. Original max: {self.class_names[np.argmax(predictions)]} -> Filtered max: {self.class_names[final_index]}")
            else:
                print(f"DEBUG: V7 No labels found for crop '{crop_name}'. Using global argmax.")

        confidence = float(predictions[final_index])
        diagnosis = self.class_names[final_index]
        
        # Heuristic severity calculation
        severity_score = confidence if "Healthy" not in diagnosis else 0.05
        
        # Create probability map
        prob_map = {self.class_names[i]: float(predictions[i]) for i in range(len(self.class_names))}
        
        return {
            "disease_name": diagnosis,
            "confidence": confidence,
            "probabilities": prob_map,
            "severity": severity_score,
            "is_v7": True,
            "model_type": "keras_38_class_filtered"
        }
