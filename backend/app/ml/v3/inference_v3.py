import torch
import cv2
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2
from .model_v3 import AgriSOTANet
import os

class AgriInference:
    def __init__(self, model_path: str, device: str = "cpu"):
        self.device = torch.device(device)
        self.model = AgriSOTANet(num_classes=38, pretrained=False).to(self.device)
        
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        
        self.model.eval()
        self.transform = A.Compose([
            A.Resize(224, 224),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ToTensorV2(),
        ])

    @torch.no_grad()
    def predict(self, image_path: str):
        # Load and Preprocess
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        augmented = self.transform(image=image)
        input_tensor = augmented['image'].unsqueeze(0).to(self.device)
        
        # Inference
        outputs = self.model(input_tensor)
        
        # Post-process
        logits = outputs['logits']
        severity = outputs['severity'].item()
        
        probs = torch.softmax(logits, dim=1)
        confidence, pred_idx = torch.max(probs, 1)
        
        return {
            "label_idx": pred_idx.item(),
            "confidence": confidence.item(),
            "severity_percentage": severity * 100
        }

if __name__ == "__main__":
    # Example Usage
    detector = AgriInference("agrisota_best.pth")
    # result = detector.predict("field_sample.jpg")
    print("Inference engine initialized correctly.")
