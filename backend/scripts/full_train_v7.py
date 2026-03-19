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
import torchvision.transforms as T
import timm
from PIL import Image

# --- MODEL DEFINITION ---
class AgriEnsembleV7_SelfContained(nn.Module):
    def __init__(self, num_classes=4, pretrained=True):
        super(AgriEnsembleV7_SelfContained, self).__init__()
        self.effnet = timm.create_model('efficientnet_b0', pretrained=pretrained, num_classes=num_classes)
        self.mobilenet = timm.create_model('mobilenetv3_small_100', pretrained=pretrained, num_classes=num_classes)

    def forward(self, x):
        return {"eff_logits": self.effnet(x), "mobile_logits": self.mobilenet(x)}

# --- DATASET DEFINITION ---
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
        try:
            image = Image.open(img_path).convert('RGB')
        except:
            image = Image.fromarray(np.ones((224, 224, 3), dtype=np.uint8) * 255)
            
        target = row['target_label']
        if self.transform:
            image = self.transform(image)
        return image, torch.tensor(target, dtype=torch.long)

# --- TRANSFORMS (Torchvision) ---
def get_transforms(img_size=224):
    train = T.Compose([
        T.RandomResizedCrop(img_size),
        T.RandomHorizontalFlip(),
        T.RandomRotation(20),
        T.ColorJitter(brightness=0.2, contrast=0.2),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    val = T.Compose([
        T.Resize((img_size, img_size)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return train, val

# --- TRAINING LOGIC ---
def train_one_epoch(model, loader, optimizer, criterion, device):
    model.train()
    running_loss = 0.0
    pbar = tqdm(loader, desc="Training")
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs['eff_logits'], labels) + criterion(outputs['mobile_logits'], labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        pbar.set_postfix({'loss': f'{loss.item():.4f}'})
    return running_loss / len(loader)

def validate(model, loader, device):
    model.eval()
    all_preds, all_labels = [], []
    with torch.no_grad():
        for images, labels in tqdm(loader, desc="Validating"):
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
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
    train_trans, val_trans = get_transforms()
    full_dataset = AgriDatasetV7(csv_path, img_dir, transform=train_trans)
    train_size = int(0.8 * len(full_dataset))
    train_ds, val_ds = random_split(full_dataset, [train_size, len(full_dataset)-train_size])
    
    target_counts = full_dataset.metadata['target_label'].value_counts().sort_index()
    weights = (1.0 / torch.tensor(target_counts.values, dtype=torch.float32))
    weights = weights / weights.sum() * 4
    weights[0] *= 0.8 # Favor disease detection
    print(f"Weights: {weights}")
    
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=32, shuffle=False)
    
    model = AgriEnsembleV7_SelfContained(num_classes=4).to(device)
    optimizer = optim.Adam(model.parameters(), lr=1e-4)
    criterion = nn.CrossEntropyLoss(weight=weights.to(device))
    
    best_f1 = 0
    for epoch in range(10):
        loss = train_one_epoch(model, train_loader, optimizer, criterion, device)
        report = validate(model, val_loader, device)
        f1 = report['weighted avg']['f1-score']
        print(f"Epoch {epoch+1}/10: Loss={loss:.4f}, Val F1={f1:.4f}")
        if f1 > best_f1:
            best_f1 = f1
            torch.save(model.state_dict(), "agrinet_ensemble_v7_best.pth")
            print("Model saved!")

if __name__ == "__main__":
    main()
