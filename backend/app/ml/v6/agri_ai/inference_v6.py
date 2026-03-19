import torch
import cv2
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2
from .model.swin_classifier import AgriNetX
import os
import json
from typing import Dict, Any, Optional

class AgriInferenceV6:
    """
    AgroCure AI Optimized Inference Engine (v6)
    Implements:
    - Swin-V2 Base Backbone (384x384)
    - Two-Stage Classification (Binary Gatekeeper + Disease Expert)
    - 80% Confidence Thresholding
    """
    def __init__(
        self, 
        model_path: str, 
        device: str = "cpu",
        num_crops: int = 14,
        num_diseases: int = 38
    ):
        self.device = torch.device(device)
        self.model = AgriNetX(
            num_crop_classes=num_crops, 
            num_disease_classes=num_diseases
        ).to(self.device)
        
        if os.path.exists(model_path):
            try:
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                print(f"AgriNet-X v6 weights loaded from {model_path}")
            except Exception as e:
                print(f"Error loading v6 weights: {e}")
        
        self.model.eval()
        
        # Consistent label mapping
        self.disease_map = {}
        # We attempt to find the disease_map.json relative to the model or in a known location
        mapping_path = os.path.join(os.path.dirname(model_path), "..", "data", "disease_map.json")
        if not os.path.exists(mapping_path):
             mapping_path = "backend/app/ml/v6/agri_ai/data/disease_map.json"
             
        if os.path.exists(mapping_path):
            with open(mapping_path, 'r') as f:
                raw_map = json.load(f)
                self.disease_map = {int(v): k for k, v in raw_map.items()}
        
        # 384x384 standard transform for Swin-V2
        self.transform = A.Compose([
            A.Resize(384, 384),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ToTensorV2(),
        ])

    @torch.no_grad()
    def predict(self, image_bytes: bytes, crop_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Runs Hierarchical Inference.
        """
        # 1. Preprocess
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            return {"error": "Invalid image data"}
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        augmented = self.transform(image=image)
        input_tensor = augmented['image'].unsqueeze(0).to(self.device)
        
        # Mock weather/soil as they aren't available in real-time during image-only scan
        weather = torch.zeros(1, 3).to(self.device)
        soil = torch.zeros(1, 4).to(self.device)
        
        # 2. Inference
        outputs = self.model(input_tensor, weather, soil)
        
        # Stage 1: Binary Gatekeeper (Healthy vs Diseased)
        # binary_head output is logit, so > 0 means Diseased
        binary_logit = outputs['binary'].item()
        is_diseased = binary_logit > 0
        
        # Stage 2: Disease Expert
        disease_probs = torch.softmax(outputs['disease_logits'], dim=1) if 'disease_logits' in outputs else torch.softmax(outputs['disease'], dim=1)
        disease_conf, disease_idx = torch.max(disease_probs, 1)
        disease_conf = disease_conf.item()
        
        # Stage 3: Crop Cross-Check
        crop_probs = torch.softmax(outputs['crop'], dim=1)
        crop_conf, crop_idx = torch.max(crop_probs, 1)
        
        # 3. Decision Logic
        if not is_diseased:
            return {
                "disease_name": "Healthy",
                "confidence": 1.0 - torch.sigmoid(outputs['binary']).item(),
                "status": "Healthy",
                "severity": 0.0
            }
        
        label = self.disease_map.get(disease_idx.item(), "Unknown Disease")
        
        # Handle Confidence Threshold (Objective 7)
        status = "Success"
        if disease_conf < 0.8:
            status = "Uncertain"
            label = f"Potential {label.split('__')[-1].replace('_',' ')}" if "__" in label else "Potential Disease"
            
        return {
            "disease_name": label,
            "confidence": disease_conf,
            "status": status,
            "severity": outputs['severity'].item(),
            "is_diseased": True,
            "binary_logit": binary_logit
        }
