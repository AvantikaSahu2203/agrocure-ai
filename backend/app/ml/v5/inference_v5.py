import torch
import cv2
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2
from .model_v5 import AgriNetV5
import os
import json

class AgriInferenceV5:
    """
    AgroCure AI Inference Engine v5
    Implements 384x384 resolution and 80% confidence thresholds.
    """
    def __init__(
        self, 
        model_path: str, 
        device: str = "cpu",
        num_crops: int = 20,
        num_diseases: int = 150
    ):
        self.device = torch.device(device)
        self.classifier = AgriNetV5(
            num_crops=num_crops, 
            num_diseases=num_diseases, 
            pretrained=False
        ).to(self.device)
        
        if os.path.exists(model_path):
            try:
                self.classifier.load_state_dict(torch.load(model_path, map_location=self.device))
            except Exception as e:
                print(f"Error loading model weights: {e}")
        self.classifier.eval()
        
        # Load Class Mapping
        self.disease_map = {}
        mapping_path = os.path.join(os.path.dirname(model_path), "data", "disease_map.json")
        if os.path.exists(mapping_path):
            with open(mapping_path, 'r') as f:
                raw_map = json.load(f)
                # Reverse the map: index -> name
                self.disease_map = {int(v): k for k, v in raw_map.items()}
        else:
            print(f"Warning: Disease map not found at {mapping_path}")
        
        # Improved 384x384 transform
        self.transform = A.Compose([
            A.LongestMaxSize(max_size=384, interpolation=cv2.INTER_CUBIC),
            A.PadIfNeeded(min_height=384, min_width=384, border_mode=cv2.BORDER_CONSTANT, value=0),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ToTensorV2(),
        ])

    @torch.no_grad()
    def predict(self, image: np.ndarray):
        """
        Runs prediction with confidence logic.
        """
        # Preprocess
        augmented = self.transform(image=image)
        input_tensor = augmented['image'].unsqueeze(0).to(self.device)
        
        # Inference
        outputs = self.classifier(input_tensor)
        
        # Disease Prediction
        disease_probs = torch.softmax(outputs['disease_logits'], dim=1)
        disease_conf, disease_idx = torch.max(disease_probs, 1)
        disease_conf = disease_conf.item()
        
        # Logic for User Requirements
        status = "Success"
        message = ""
        
        if disease_conf < 0.8:
            status = "Uncertain"
            message = "Possible disease detected – please capture clearer image."
            label = "Potential Disease – Further Analysis Required"
        else:
            # Map index to name
            label = self.disease_map.get(disease_idx.item(), f"Detected: {disease_idx.item()}")
            # Clean label (e.g., "Tomato__Early_Blight" -> "Early Blight")
            if "__" in label:
                label = label.split("__")[1].replace("_", " ")
            
        return {
            "status": status,
            "message": message,
            "prediction": label,
            "confidence": disease_conf,
            "severity": outputs['severity'].item()
        }
