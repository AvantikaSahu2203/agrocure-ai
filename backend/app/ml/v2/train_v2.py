import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np
from .model_v2 import get_model

class CropDiseaseLoss(nn.Module):
    """
    Combined Loss: CrossEntropy (Class) + MSE (Severity) + Dice (Segmentation)
    """
    def __init__(self, w_cls=1.0, w_sev=0.5, w_seg=0.5):
        super(CropDiseaseLoss, self).__init__()
        self.cls_loss = nn.CrossEntropyLoss()
        self.sev_loss = nn.MSELoss()
        self.w_cls = w_cls
        self.w_sev = w_sev
        self.w_seg = w_seg
        
    def dice_loss(self, pred, target):
        smooth = 1.0
        iflat = pred.view(-1)
        tflat = target.view(-1)
        intersection = (iflat * tflat).sum()
        return 1 - ((2. * intersection + smooth) / (iflat.sum() + tflat.sum() + smooth))

    def forward(self, outputs, targets):
        # outputs: dict from model
        # targets: dict with 'class', 'severity', 'mask'
        
        l_cls = self.cls_loss(outputs['classification'], targets['class'])
        l_sev = self.sev_loss(outputs['severity'], targets['severity'])
        l_seg = self.dice_loss(outputs['segmentation'], targets['mask'])
        
        total_loss = (self.w_cls * l_cls) + (self.w_sev * l_sev) + (self.w_seg * l_seg)
        
        return {
            "total": total_loss,
            "cls": l_cls,
            "sev": l_sev,
            "seg": l_seg
        }

def train_one_epoch(model, loader, optimizer, criterion, device):
    model.train()
    losses = []
    
    for images, labels in loader:
        images = images.to(device)
        # Move target tensors to device
        targets = {k: v.to(device) for k, v in labels.items()}
        
        optimizer.zero_grad()
        outputs = model(images)
        loss_dict = criterion(outputs, targets)
        
        loss_dict['total'].backward()
        optimizer.step()
        
        losses.append(loss_dict['total'].item())
        
    return np.mean(losses)

def validate(model, loader, criterion, device):
    model.eval()
    losses = []
    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            targets = {k: v.to(device) for k, v in labels.items()}
            outputs = model(images)
            loss_dict = criterion(outputs, targets)
            losses.append(loss_dict['total'].item())
            
    return np.mean(losses)

def run_training_pipeline(num_classes, train_loader, val_loader, epochs=50):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = get_model(num_classes).to(device)
    
    # Optimizer: AdamW handles weight decay better for transformers
    optimizer = optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-2)
    
    # Scheduler: Cosine Annealing with Warmup
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    
    criterion = CropDiseaseLoss()
    
    best_loss = float('inf')
    
    for epoch in range(epochs):
        train_loss = train_one_epoch(model, train_loader, optimizer, criterion, device)
        val_loss = validate(model, val_loader, criterion, device)
        scheduler.step()
        
        print(f"Epoch {epoch+1}/{epochs} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")
        
        if val_loss < best_loss:
            best_loss = val_loss
            torch.save(model.state_dict(), "transagronet_best.pth")
            print("--- Model Saved ---")

    print("\nTraining Complete. Best Model Exported.")
    return model
