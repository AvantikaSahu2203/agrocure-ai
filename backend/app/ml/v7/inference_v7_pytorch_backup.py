import torch
import cv2
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2
from .ensemble_model import AgriEnsembleV7
import os

class AgriInferenceV7:
    """
    AgroCure AI Ensemble Inference v7
    Combines EfficientNet-B0 and MobileNetV3-Small.
    """
    def __init__(self, model_path: str, device: str = "cpu"):
        print(f"DEBUG: AgriInferenceV7 - Initializing with model_path: {model_path}")
        self.device = torch.device(device)
        try:
            self.model = AgriEnsembleV7(num_classes=4, pretrained=False).to(self.device)
            print("DEBUG: AgriEnsembleV7 instance created.")
        except Exception as e:
            print(f"DEBUG: AgriEnsembleV7 creation FAILED: {e}")
            raise
        
        if os.path.exists(model_path):
            try:
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                print("DEBUG: Weights loaded successfully.")
            except Exception as e:
                print(f"DEBUG: Weights loading FAILED: {e}")
                raise
        else:
            print(f"DEBUG: Weights path NOT FOUND: {model_path}")
        
        # Standard input size for v7 is 224x224
        self.transform = A.Compose([
            A.Resize(224, 224),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ToTensorV2(),
        ])
        
        self.class_names = ["Healthy", "Blight", "Powdery Mildew", "Leaf Spot"]

    @torch.no_grad()
    def predict(self, image_bytes: bytes, crop_name: str = None):
        """
        Takes image bytes and returns detailed prediction.
        """
        # Load image
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
             raise ValueError("Could not decode image bytes")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Transform
        augmented = self.transform(image=image)
        input_tensor = augmented['image'].unsqueeze(0).to(self.device)
        
        # Inference
        outputs = self.model(input_tensor)
        
        # Average Logits (Ensemble logic)
        avg_logits = (outputs['eff_logits'] + outputs['mobile_logits']) / 2
        probs_tensor = torch.softmax(avg_logits, dim=1)
        probs = probs_tensor.cpu().numpy()[0]
        
        confidence = float(np.max(probs))
        idx = int(np.argmax(probs))
        
        # Severity calculation (heuristic based on logits strength)
        severity_score = float(torch.sigmoid(avg_logits.max()).item())
        
        # Map all probabilities to class names
        prob_map = {self.class_names[i]: float(probs[i]) for i in range(len(self.class_names))}
        
        return {
            "disease_name": self.class_names[idx],
            "confidence": confidence,
            "probabilities": prob_map,
            "severity": severity_score,
            "is_v7": True
        }
