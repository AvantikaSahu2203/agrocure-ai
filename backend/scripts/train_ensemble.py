import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
import os
import cv2
from tqdm import tqdm
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
import albumentations as A
from albumentations.pytorch import ToTensorV2

import sys
sys.path.append(os.getcwd())

import timm

class AgriEnsembleV7(nn.Module):
    """
    AgroCure AI Ensemble v7
    Combines:
    - EfficientNet-B0 (Texture & Detail)
    - MobileNetV3-Small (Speed & Lightweight)
    
    Targeting 4 classes: Healthy, Blight, Powdery Mildew, Leaf Spot
    """
    def __init__(self, num_classes=4, pretrained=True):
        super(AgriEnsembleV7, self).__init__()
        
        # 1. EfficientNet-B0
        self.effnet = timm.create_model(
            'efficientnet_b0', 
            pretrained=pretrained, 
            num_classes=num_classes
        )
        
        # 2. MobileNetV3-Small
        self.mobilenet = timm.create_model(
            'mobilenetv3_small_100', 
            pretrained=pretrained, 
            num_classes=num_classes
        )

    def forward(self, x):
        out_eff = self.effnet(x)
        out_mobile = self.mobilenet(x)
        
        return {
            "eff_logits": out_eff,
            "mobile_logits": out_mobile
        }

class AgriDatasetV7(torch.utils.data.Dataset):
    def __init__(self, csv_file, root_dir, transform=None):
        self.metadata = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, idx):
        row = self.metadata.iloc[idx]
        img_path = os.path.join(self.root_dir, row['image_path'])
        
        image = cv2.imread(img_path)
        if image is None:
            # Fallback for missing images
            image = np.ones((224, 224, 3), dtype=np.uint8) * 255
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
        target = row['target_label']
        
        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']
            
        return image, torch.tensor(target, dtype=torch.long)

def get_transforms(img_size=224):
    train = A.Compose([
        A.RandomResizedCrop(img_size, img_size),
        A.HorizontalFlip(p=0.5),
        A.Rotate(limit=20, p=0.5),
        A.RandomBrightnessContrast(p=0.5),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])
    val = A.Compose([
        A.Resize(img_size, img_size),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])
    return train, val

def train_one_epoch(model, loader, optimizer, criterion, device):
    model.train()
    running_loss = 0.0
    pbar = tqdm(loader, desc="Training")
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        
        outputs = model(images)
        loss_eff = criterion(outputs['eff_logits'], labels)
        loss_mobile = criterion(outputs['mobile_logits'], labels)
        
        loss = loss_eff + loss_mobile
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        pbar.set_postfix({'loss': f'{loss.item():.4f}'})
    return running_loss / len(loader)

def validate(model, loader, device):
    model.eval()
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for images, labels in tqdm(loader, desc="Validating"):
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            # Ensemble average
            avg_logits = (outputs['eff_logits'] + outputs['mobile_logits']) / 2
            preds = torch.argmax(avg_logits, dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    return classification_report(all_labels, all_preds, output_dict=True, zero_division=0)

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    csv_path = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\dataset_unified\train_metadata_v7.csv"
    img_dir = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\dataset_unified"
    
    if not os.path.exists(csv_path):
        print(f"Error: Missing {csv_path}. Please run prepare_4class_metadata.py first.")
        return

    train_trans, val_trans = get_transforms()
    
    full_dataset = AgriDatasetV7(csv_path, img_dir, transform=train_trans)
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_ds, val_ds = random_split(full_dataset, [train_size, val_size])
    
    # Class weights for loss
    target_counts = full_dataset.metadata['target_label'].value_counts().sort_index()
    weights = 1.0 / torch.tensor(target_counts.values, dtype=torch.float32)
    weights = weights / weights.sum() * 4
    # Slightly favor undersampled classes and penalize False Neutrals (Healthy)
    weights[0] = weights[0] * 0.8 
    
    print(f"Class counts: {target_counts.to_dict()}")
    print(f"Calculated Class weights: {weights}")
    
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=32, shuffle=False)
    
    model = AgriEnsembleV7(num_classes=4).to(device)
    optimizer = optim.Adam(model.parameters(), lr=1e-4)
    criterion = nn.CrossEntropyLoss(weight=weights.to(device))
    
    best_f1 = 0
    epochs = 10 
    for epoch in range(epochs):
        loss = train_one_epoch(model, train_loader, optimizer, criterion, device)
        report = validate(model, val_loader, device)
        f1 = report['weighted avg']['f1-score']
        print(f"\nEpoch {epoch+1}/{epochs}:")
        print(f"  Train Loss: {loss:.4f}")
        print(f"  Val F1-Score: {f1:.4f}")
        
        if f1 > best_f1:
            best_f1 = f1
            torch.save(model.state_dict(), "agrinet_ensemble_v7_best.pth")
            print("  [✓] Model checkpoint saved.")

if __name__ == "__main__":
    main()
