import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm
import numpy as np
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix
import time

# Use our SOTA components
from .model_v3 import AgriSOTANet
from .dataset_v3 import AgriDataset, get_train_transforms, get_val_transforms

class AgriTrainer:
    def __init__(self, model, train_loader, val_loader, device="cuda"):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = device
        
        # 1. Optimizer: AdamW
        self.optimizer = optim.AdamW(self.model.parameters(), lr=1e-4, weight_decay=1e-2)
        
        # 2. Scheduler: Cosine Annealing
        self.scheduler = optim.lr_scheduler.CosineAnnealingLR(self.optimizer, T_max=10, eta_min=1e-6)
        
        # 3. Loss: Cross-Entropy with Label Smoothing + MSE for Severity
        self.criterion_cls = nn.CrossEntropyLoss(label_smoothing=0.1)
        self.criterion_sev = nn.MSELoss()
        
        # 4. Mixed Precision Scaler
        self.scaler = torch.amp.GradScaler('cuda') if device == "cuda" else None

    def train_epoch(self):
        self.model.train()
        total_loss = 0
        pbar = tqdm(self.train_loader, desc="Training")
        
        for batch in pbar:
            images = batch['image'].to(self.device)
            labels = batch['label'].to(self.device)
            severities = batch['severity'].to(self.device)
            
            self.optimizer.zero_grad()
            
            # Using Managed Mixed Precision
            if self.scaler:
                with torch.amp.autocast('cuda'):
                    outputs = self.model(images)
                    loss_cls = self.criterion_cls(outputs['logits'], labels)
                    loss_sev = self.criterion_sev(outputs['severity'].squeeze(), severities)
                    loss = loss_cls + 0.5 * loss_sev
                    
                self.scaler.scale(loss).backward()
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                outputs = self.model(images)
                loss_cls = self.criterion_cls(outputs['logits'], labels)
                loss_sev = self.criterion_sev(outputs['severity'].squeeze(), severities)
                loss = loss_cls + 0.5 * loss_sev
                loss.backward()
                self.optimizer.step()
                
            total_loss += loss.item()
            pbar.set_postfix({'loss': f'{loss.item():.4f}'})
            
        return total_loss / len(self.train_loader)

    def validate(self):
        self.model.eval()
        all_labels = []
        all_preds = []
        val_loss = 0
        
        with torch.no_grad():
            for batch in self.val_loader:
                images = batch['image'].to(self.device)
                labels = batch['label'].to(self.device)
                severities = batch['severity'].to(self.device)
                
                outputs = self.model(images)
                loss_cls = self.criterion_cls(outputs['logits'], labels)
                loss_sev = self.criterion_sev(outputs['severity'].squeeze(), severities)
                val_loss += (loss_cls + 0.5 * loss_sev).item()
                
                _, preds = torch.max(outputs['logits'], 1)
                all_labels.extend(labels.cpu().numpy())
                all_preds.extend(preds.cpu().numpy())
                
        acc = accuracy_score(all_labels, all_preds)
        f1 = f1_score(all_labels, all_preds, average='weighted')
        
        return val_loss / len(self.val_loader), acc, f1

    def run(self, num_epochs=10):
        print(f"Starting Training for {num_epochs} epochs on {self.device}...")
        best_f1 = 0
        
        for epoch in range(num_epochs):
            train_loss = self.train_epoch()
            val_loss, acc, f1 = self.validate()
            self.scheduler.step()
            
            print(f"Epoch {epoch+1}/{num_epochs}:")
            print(f"  Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")
            print(f"  Accuracy: {acc:.4f} | F1 Score: {f1:.4f}")
            
            if f1 > best_f1:
                best_f1 = f1
                torch.save(self.model.state_dict(), "agrisota_best.pth")
                print("  [Saved Best Model]")

if __name__ == "__main__":
    # Mock Training Run
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Dummy data
    dummy_paths = ["dummy.jpg"] * 20
    dummy_labels = np.random.randint(0, 38, size=20).tolist()
    dummy_severities = np.random.uniform(0, 1, size=20).tolist()
    
    # Create dummy image
    import cv2
    cv2.imwrite("dummy.jpg", np.zeros((224, 224, 3), dtype=np.uint8))
    
    train_ds = AgriDataset(dummy_paths, dummy_labels, dummy_severities, transform=get_train_transforms())
    val_ds = AgriDataset(dummy_paths, dummy_labels, dummy_severities, transform=get_val_transforms())
    
    train_loader = DataLoader(train_ds, batch_size=4, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=4)
    
    model = AgriSOTANet(num_classes=38)
    trainer = AgriTrainer(model, train_loader, val_loader, device=device)
    
    trainer.run(num_epochs=1)
    
    # Cleanup
    import os
    if os.path.exists("dummy.jpg"):
        os.remove("dummy.jpg")
