from ultralytics import YOLO
import os
import cv2
import torch
from typing import List, Tuple

class LesionDetector:
    """
    YOLOv10-based lesion detector for localization.
    Helps the system focus on specific disease areas rather than the whole leaf.
    """
    def __init__(self, model_path: str = "yolov10n.pt"):
        # Load YOLOv10 model (falls back to downloading if not present)
        self.model = YOLO(model_path)
        
    def detect_lesions(self, image_path: str, conf: float = 0.25) -> List[Tuple[int, int, int, int]]:
        """
        Detect lesions and return bounding boxes [x1, y1, x2, y2].
        """
        results = self.model(image_path, conf=conf)
        boxes = []
        for result in results:
            for box in result.boxes:
                # Get coordinates
                b = box.xyxy[0].cpu().numpy().astype(int)
                boxes.append(tuple(b))
        return boxes

    def crop_lesions(self, image: cv2.Mat, boxes: List[Tuple[int, int, int, int]], padding: int = 10) -> List[cv2.Mat]:
        """
        Crop detected lesion regions from the image.
        """
        crops = []
        h, w = image.shape[:2]
        for (x1, y1, x2, y2) in boxes:
            # Apply padding
            x1 = max(0, x1 - padding)
            y1 = max(0, y1 - padding)
            x2 = min(w, x2 + padding)
            y2 = min(h, y2 + padding)
            
            crop = image[y1:y2, x1:x2]
            crops.append(crop)
        return crops

if __name__ == "__main__":
    # detector = LesionDetector()
    # print("YOLOv10 Detector Ready.")
    pass
