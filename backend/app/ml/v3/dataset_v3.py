import torch
from torch.utils.data import Dataset, DataLoader
import cv2
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2
import os
from typing import List, Tuple, Optional

class AgriDataset(Dataset):
    """
    Production-grade Dataset for multi-crop disease detection.
    Supports real-field image augmentations and multi-task labels.
    """
    def __init__(self, image_paths: List[str], labels: List[int], severities: List[float], transform: Optional[A.Compose] = None):
        self.image_paths = image_paths
        self.labels = labels
        self.severities = severities
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        label = self.labels[idx]
        severity = self.severities[idx]
        
        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']
            
        return {
            'image': image,
            'label': torch.tensor(label, dtype=torch.long),
            'severity': torch.tensor(severity, dtype=torch.float32)
        }

def get_train_transforms(img_size: int = 224):
    """
    Advanced augmentation pipeline for real-field robustness.
    Includes shadow simulation, ISO noise, and motion blur.
    """
    return A.Compose([
        A.Resize(img_size, img_size),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.2),
        A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=30, p=0.5),
        
        # Real-field condition simulations
        A.OneOf([
            A.MotionBlur(p=0.2),
            A.MedianBlur(blur_limit=3, p=0.1),
            A.Blur(blur_limit=3, p=0.1),
        ], p=0.3),
        
        A.OneOf([
            A.ISONoise(p=0.2),
            A.GaussNoise(p=0.2),
        ], p=0.3),
        
        # Environmental Simulation
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
        A.HueSaturationValue(hue_shift_limit=10, sat_shift_limit=20, val_shift_limit=10, p=0.3),
        
        # Shadow Simulation (Crucial for field images)
        A.RandomShadow(num_shadows_upper=3, shadow_dimension=5, p=0.3),
        
        # Quality degradation (Low-res/JPEG artifacts)
        A.ImageCompression(quality_lower=60, quality_upper=90, p=0.2),
        
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])

def get_val_transforms(img_size: int = 224):
    return A.Compose([
        A.Resize(img_size, img_size),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])

if __name__ == "__main__":
    # Test DataLoader
    print("Testing AgriDataset Pipeline...")
    dummy_paths = ["dummy.jpg"] * 10
    dummy_labels = [0] * 10
    dummy_severities = [0.5] * 10
    
    # Check if a dummy file exists, if not create a black one for testing
    if not os.path.exists("dummy.jpg"):
        cv2.imwrite("dummy.jpg", np.zeros((300, 300, 3), dtype=np.uint8))
        
    dataset = AgriDataset(dummy_paths, dummy_labels, dummy_severities, transform=get_train_transforms())
    loader = DataLoader(dataset, batch_size=2, shuffle=True)
    
    batch = next(iter(loader))
    print(f"Batch Image Shape: {batch['image'].shape}")
    print(f"Batch Label Shape: {batch['label'].shape}")
    print(f"Batch Severity Shape: {batch['severity'].shape}")
    
    # Cleanup
    if os.path.exists("dummy.jpg"):
        os.remove("dummy.jpg")
