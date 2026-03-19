import torch
from torch.utils.data import Dataset
import cv2
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2
from typing import List, Optional

class AgriDatasetV5(Dataset):
    """
    AgroCure AI Dataset v5
    Designed for 384x384 resolution and high-detail lesion preservation.
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
            image = np.zeros((384, 384, 3), dtype=np.uint8)
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

def get_v5_train_transforms(img_size: int = 384):
    """
    Aggressive augmentation to reduce 'Healthy' bias and handle farm variations.
    """
    return A.Compose([
        A.LongestMaxSize(max_size=img_size, interpolation=cv2.INTER_CUBIC),
        A.PadIfNeeded(min_height=img_size, min_width=img_size, border_mode=cv2.BORDER_CONSTANT, value=0),
        
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.5),
        A.RandomRotate90(p=0.5),
        A.Transpose(p=0.2),
        
        A.OneOf([
            A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=1),
            A.HueSaturationValue(p=1),
            A.RGBShift(p=1),
        ], p=0.5),
        
        A.OneOf([
            A.GaussNoise(var_limit=(10.0, 50.0), p=1),
            A.GaussianBlur(blur_limit=(3, 7), p=1),
        ], p=0.3),
        
        A.OneOf([
            A.OpticalDistortion(p=1),
            A.GridDistortion(p=1),
            A.PiecewiseAffine(p=1),
        ], p=0.2),
        
        A.CoarseDropout(max_holes=8, max_height=img_size//10, max_width=img_size//10, p=0.3),
        A.RandomShadow(p=0.3),
        
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])

def get_v5_val_transforms(img_size: int = 384):
    return A.Compose([
        A.LongestMaxSize(max_size=img_size, interpolation=cv2.INTER_CUBIC),
        A.PadIfNeeded(min_height=img_size, min_width=img_size, border_mode=cv2.BORDER_CONSTANT, value=0),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])
