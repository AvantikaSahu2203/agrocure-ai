import torch
from torch.utils.data import Dataset, DataLoader
import cv2
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2
import os
from typing import List, Tuple, Optional, Dict

class AgriDatasetV4(Dataset):
    """
    Advanced Dataset for hierarchical crop disease detection.
    Supports Crop Type, Disease Class, and Severity.
    """
    def __init__(
        self, 
        image_paths: List[str], 
        crop_labels: List[int],
        disease_labels: List[int], 
        severities: List[float], 
        transform: Optional[A.Compose] = None
    ):
        self.image_paths = image_paths
        self.crop_labels = crop_labels
        self.disease_labels = disease_labels
        self.severities = severities
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = cv2.imread(img_path)
        if image is None:
            # Fallback for missing files in development
            image = np.zeros((224, 224, 3), dtype=np.uint8)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        crop_label = self.crop_labels[idx]
        disease_label = self.disease_labels[idx]
        severity = self.severities[idx]
        
        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']
            
        return {
            'image': image,
            'crop_label': torch.tensor(crop_label, dtype=torch.long),
            'disease_label': torch.tensor(disease_label, dtype=torch.long),
            'severity': torch.tensor(severity, dtype=torch.float32)
        }

def get_v4_train_transforms(img_size: int = 224):
    """
    State-of-the-art augmentation pipeline for agricultural field images.
    """
    return A.Compose([
        A.Resize(img_size, img_size),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.2),
        A.RandomRotate90(p=0.2),
        A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.2, rotate_limit=45, p=0.5),
        
        # Weather and Lighting simulations
        A.OneOf([
            A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=1),
            A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=1),
            A.CLAHE(clip_limit=4.0, tile_grid_size=(8, 8), p=1),
        ], p=0.6),
        
        # Field conditions: Blur, Noise, Shadow
        A.OneOf([
            A.MotionBlur(p=0.2),
            A.GaussNoise(p=0.2),
            A.ISONoise(p=0.2),
        ], p=0.4),
        
        A.RandomShadow(num_shadows_upper=4, shadow_dimension=5, p=0.4),
        A.ImageCompression(quality_lower=50, quality_upper=95, p=0.3),
        
        # Normalization
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])

def get_v4_val_transforms(img_size: int = 224):
    return A.Compose([
        A.Resize(img_size, img_size),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])
