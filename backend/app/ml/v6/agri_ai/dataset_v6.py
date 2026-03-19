import os
import cv2
import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset, WeightedRandomSampler
import albumentations as A
from albumentations.pytorch import ToTensorV2
from typing import Optional

class AgriDatasetV6(Dataset):
    """
    AgroCure AI Dataset v6 (AgriNet-X ready)
    Loads from unified metadata CSV and implements multi-head targets.
    """
    def __init__(self, csv_file: str, root_dir: str, transform: Optional[A.Compose] = None):
        self.metadata = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform
        
        # Consistent label mapping for disease
        self.disease_classes = sorted(self.metadata['normalized_label'].unique())
        self.disease_to_idx = {cls: i for i, cls in enumerate(self.disease_classes)}
        
        # Mapping for crops (extracted from label prefix, e.g., 'Tomato__Early_Blight' -> 'Tomato')
        self.crop_classes = sorted(list(set([label.split('__')[0] for label in self.disease_classes])))
        self.crop_to_idx = {cls: i for i, cls in enumerate(self.crop_classes)}

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, idx):
        row = self.metadata.iloc[idx]
        img_path = os.path.join(self.root_dir, row['image_path'])
        
        image = cv2.imread(img_path)
        if image is None:
            # Fallback to white image if path fails
            image = np.ones((512, 512, 3), dtype=np.uint8) * 255
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
        full_label = row['normalized_label']
        crop_name = full_label.split('__')[0]
        
        disease_idx = self.disease_to_idx[full_label]
        crop_idx = self.crop_to_idx[crop_name]
        
        # Two-Stage Logic: Binary Classification (Healthy vs Diseased)
        is_diseased = 0 if "__healthy" in full_label.lower() or "healthy" in full_label.lower() else 1
        
        # Severity estimation (mocked as 0.0 for now if not in CSV)
        severity = row.get('severity', 0.0)
        
        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']
            
        return {
            'image': image,
            'crop_label': torch.tensor(crop_idx, dtype=torch.long),
            'disease_label': torch.tensor(disease_idx, dtype=torch.long),
            'is_diseased': torch.tensor(is_diseased, dtype=torch.float32), # Binary label
            'severity': torch.tensor(severity, dtype=torch.float32)
        }

def get_v6_train_transforms(img_size: int = 512):
    """
    EXPERT-RECOMMENDED AUGMENTATION PIPELINE (AgriNet-X)
    Simulates real farm conditions: sunlight, haze, noise, distortion.
    """
    return A.Compose([
        A.RandomResizedCrop(img_size, img_size, scale=(0.7, 1.0), p=0.5),
        
        # Texture & Pattern Awareness (Objective 3 & 4)
        A.OneOf([
            A.Sharpen(alpha=(0.2, 0.5), p=1),
            A.Emboss(alpha=(0.2, 0.5), p=1),
        ], p=0.3),
        A.ElasticTransform(sigma=50, alpha=1, alpha_affine=10, p=0.2), # Simulates leaf wilting/texture abnormalties
        
        # Real-world Weather & Lighting
        A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=0.7),
        A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1, p=0.4),
        A.RandomShadow(p=0.4),
        A.RandomFog(fog_coef_lower=0.1, fog_coef_upper=0.3, alpha_coef=0.08, p=0.3),
        
        # Clarity & Color
        A.CLAHE(clip_limit=4.0, tile_grid_size=(8, 8), p=0.5),
        
        # Camera & Lens Artifacts
        A.OneOf([
            A.GaussNoise(var_limit=(10, 50), p=1),
            A.ISONoise(p=1),
        ], p=0.4),
        A.OneOf([
            A.MotionBlur(p=1),
            A.MedianBlur(blur_limit=3, p=1),
        ], p=0.3),
        
        # Damage & Occlusion
        A.CoarseDropout(max_holes=8, max_height=img_size//16, max_width=img_size//16, p=0.4),
        
        # Geometric
        A.HorizontalFlip(p=0.5),
        A.Rotate(limit=45, p=0.5),
        
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])

def get_v6_val_transforms(img_size: int = 512):
    return A.Compose([
        A.Resize(img_size, img_size),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])

def get_weighted_sampler(dataset: AgriDatasetV6):
    """
    Weighted sampling to address rare disease classes.
    """
    labels = dataset.metadata['normalized_label'].tolist()
    class_counts = dataset.metadata['normalized_label'].value_counts()
    
    # Weight per class = 1.0 / count
    class_weights = 1.0 / class_counts
    weights = [class_weights[label] for label in labels]
    
    return WeightedRandomSampler(weights, num_samples=len(weights), replacement=True)
