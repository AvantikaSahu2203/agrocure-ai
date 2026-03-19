from ultralytics import YOLO
import torch
import cv2
import numpy as np
import os

class AgriYOLOv8Detector:
    """
    YOLOv8 wrapper for leaf and infected spot localization.
    """
    def __init__(self, model_path: str = "yolov8n.pt", device: str = "cpu"):
        self.device = torch.device(device)
        # Load a pretrained YOLOv8 model (Nano for speed, or custom trained)
        self.model = YOLO(model_path)
        
    def detect_and_crop(self, image_path: str, save_crop: bool = False) -> np.ndarray:
        """
        Detect leaves and return the highest confidence crop.
        """
        results = self.model(image_path, device=self.device)
        
        # Original Image
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        if len(results) == 0 or len(results[0].boxes) == 0:
            # Fallback to original image if no detection
            return img
            
        # Get the box with highest confidence
        boxes = results[0].boxes
        best_box = boxes[0] # YOLOv8 sorts by confidence
        
        # Extract coordinates
        x1, y1, x2, y2 = best_box.xyxy[0].cpu().numpy().astype(int)
        
        # Crop image
        crop = img[y1:y2, x1:x2]
        
        if save_crop:
            cv2.imwrite("debug_crop.jpg", cv2.cvtColor(crop, cv2.COLOR_RGB2BGR))
            
        return crop

if __name__ == "__main__":
    # Test YOLO Integration
    # detector = AgriYOLOv8Detector()
    # print("YOLOv8 Detector initialized.")
    pass
