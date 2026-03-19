import torch
import cv2
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2
from ..v5.model_v5 import AgriNetV5
import os
import json

class AgriInferenceV6:
    """
    AgroCure AI Unified Inference Engine v6
    Predicts: Crop Type, Disease Name, Confidence Score.
    """
    def __init__(
        self, 
        model_path: str, 
        class_map_path: str,
        device: str = "cpu"
    ):
        self.device = torch.device(device)
        
        # Load Class Mapping
        with open(class_map_path, 'r') as f:
            self.class_map = json.load(f)
        
        num_crops = len(self.class_map['crops'])
        num_diseases = len(self.class_map['diseases'])
        
        # Initialize Architecture
        self.model = AgriNetV5(
            num_crops=num_crops, 
            num_diseases=num_diseases, 
            pretrained=False
        ).to(self.device)
        
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
        
        # Standard 384x384 transform
        self.transform = A.Compose([
            A.LongestMaxSize(max_size=384, interpolation=cv2.INTER_CUBIC),
            A.PadIfNeeded(min_height=384, min_width=384, border_mode=cv2.BORDER_CONSTANT, value=0),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ToTensorV2(),
        ])

    @torch.no_grad()
    def predict(self, image: np.ndarray):
        """
        Takes RGB image and returns predictions.
        """
        augmented = self.transform(image=image)
        input_tensor = augmented['image'].unsqueeze(0).to(self.device)
        
        outputs = self.model(input_tensor)
        
        # 1. Crop Type
        crop_probs = torch.softmax(outputs['crop_logits'], dim=1)
        crop_conf, crop_idx = torch.max(crop_probs, 1)
        crop_name = self.class_map['crops'][str(crop_idx.item())]
        
        # 2. Disease Name
        disease_probs = torch.softmax(outputs['disease_logits'], dim=1)
        disease_conf, disease_idx = torch.max(disease_probs, 1)
        disease_name = self.class_map['diseases'][str(disease_idx.item())]
        
        return {
            "crop": crop_name,
            "disease": disease_name,
            "confidence": float(disease_conf.item()),
            "crop_confidence": float(crop_conf.item()),
            "severity": float(outputs['severity'].item())
        }
