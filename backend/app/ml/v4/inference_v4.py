import torch
import cv2
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2
from .model_v4 import AgriNextNet
from .yolo_detector import AgriYOLOv8Detector
import os

class AgriInferenceV4:
    """
    Production Inference Engine for v4 Pipeline.
    Combines Localization (YOLOv8) + Hierarchical Classification (EfficientNetV2-L).
    """
    def __init__(
        self, 
        model_path: str, 
        yolo_path: str = "yolov8n.pt", 
        device: str = "cpu"
    ):
        self.device = torch.device(device)
        
        # 1. Initialize YOLOv8
        self.detector = AgriYOLOv8Detector(model_path=yolo_path, device=device)
        
        # 2. Initialize AgriNextNet
        self.classifier = AgriNextNet(pretrained=False).to(self.device)
        if os.path.exists(model_path):
            self.classifier.load_state_dict(torch.load(model_path, map_location=self.device))
        self.classifier.eval()
        
        # 3. Transform for Classification
        self.transform = A.Compose([
            A.Resize(224, 224),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ToTensorV2(),
        ])
        
        # Class maps (Mock - in real scenario these are loaded from a JSON)
        self.crop_map = ["Apple", "Corn", "Grape", "Potato", "Tomato", "Wheat", "Rice", "Cotton", "Mango"]
        # ... more classes

    @torch.no_grad()
    def analyze(self, image_path: str):
        # Phase 1: Localization
        crop_img = self.detector.detect_and_crop(image_path)
        
        # Phase 2: Classification Preprocessing
        augmented = self.transform(image=crop_img)
        input_tensor = augmented['image'].unsqueeze(0).to(self.device)
        
        # Phase 3: Hierarchical Inference
        outputs = self.classifier(input_tensor)
        
        # Post-process Crop
        crop_probs = torch.softmax(outputs['crop_logits'], dim=1)
        crop_conf, crop_idx = torch.max(crop_probs, 1)
        
        # Post-process Disease
        disease_probs = torch.softmax(outputs['disease_logits'], dim=1)
        disease_conf, disease_idx = torch.max(disease_probs, 1)
        
        # Severity
        severity = outputs['severity'].item()
        
        return {
            "crop_type": self.crop_map[crop_idx.item()] if crop_idx.item() < len(self.crop_map) else "Unknown",
            "crop_confidence": crop_conf.item(),
            "disease_label_idx": disease_idx.item(),
            "disease_confidence": disease_conf.item(),
            "severity_percentage": float(f"{severity * 100:.2f}"),
            "localized": True
        }

if __name__ == "__main__":
    print("AgriInferenceV4 Engine Initialized.")
