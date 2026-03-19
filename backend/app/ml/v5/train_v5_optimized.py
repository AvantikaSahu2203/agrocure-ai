import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm
import numpy as np
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, confusion_matrix
import os
import time
import pandas as pd
import json

from .model_v5 import AgriNetV5, FocalLoss
from .dataset_v5 import AgriDatasetV5, get_v5_train_transforms, get_v5_val_transforms

class EarlyStopping:
    def __init__(self, patience=5, min_delta=0, mode='max'):
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        
    def __call__(self, score):
        if self.best_score is None:
            self.best_score = score
        elif (self.mode == 'max' and score < self.best_score + self.min_delta) or \
             (self.mode == 'min' and score > self.best_score - self.min_delta):
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.counter = 0

class AgriTrainerV5Optimized:
    def __init__(
        self, 
        model, 
        train_loader, 
        val_loader, 
        device="cuda",
        class_weights=None,
        max_lr=1e-3
    ):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = device
        
        # 1. Losses
        self.criterion_disease = FocalLoss(alpha=1, gamma=2)
        self.criterion_crop = nn.CrossEntropyLoss(weight=class_weights)
        self.criterion_severity = nn.MSELoss()
        
        # 2. Optimizer & Scheduler
        # Using AdamW with OneCycleLR for faster convergence
        self.optimizer = optim.AdamW(self.model.parameters(), lr=max_lr/10, weight_decay=1e-2)
        
        # Total steps for OneCycleLR
        total_steps = len(train_loader) * 25 # Assume 25 epochs for planning
        self.scheduler = optim.lr_scheduler.OneCycleLR(
            self.optimizer, 
            max_lr=max_lr, 
            total_steps=total_steps,
            pct_start=0.3, # 30% of time warming up
            anneal_strategy='cos'
        )
        
        # 3. Mixed Precision
        self.scaler = torch.amp.GradScaler('cuda') if device == "cuda" else None
        
        # 4. Early Stopping
        self.early_stopping = EarlyStopping(patience=5, mode='max')

    def train_epoch(self, epoch):
        self.model.train()
        total_loss = 0
        pbar = tqdm(self.train_loader, desc=f"Epoch {epoch+1} Training")
        
        for batch in pbar:
            images = batch['image'].to(self.device, non_blocking=True)
            crop_labels = batch['crop_label'].to(self.device, non_blocking=True)
            disease_labels = batch['disease_label'].to(self.device, non_blocking=True)
            severities = batch['severity'].to(self.device, non_blocking=True)
            
            self.optimizer.zero_grad(set_to_none=True) # set_to_none is slightly faster
            
            with torch.amp.autocast('cuda' if self.device == "cuda" else "cpu"):
                outputs = self.model(images)
                loss_crop = self.criterion_crop(outputs['crop_logits'], crop_labels)
                loss_disease = self.criterion_disease(outputs['disease_logits'], disease_labels)
                loss_severity = self.criterion_severity(outputs['severity'].squeeze(), severities)
                
                loss = loss_crop + 2.0 * loss_disease + 0.5 * loss_severity
            
            if self.scaler:
                self.scaler.scale(loss).backward()
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                loss.backward()
                self.optimizer.step()
                
            self.scheduler.step() # Step every batch for OneCycleLR
            
            total_loss += loss.item()
            pbar.set_postfix({'loss': f'{loss.item():.4f}', 'lr': f'{self.optimizer.param_groups[0]["lr"]:.6f}'})
            
        return total_loss / len(self.train_loader)

    def evaluate(self):
        self.model.eval()
        all_d_labels = []
        all_d_preds = []
        val_loss = 0
        
        with torch.no_grad():
            for batch in self.val_loader:
                images = batch['image'].to(self.device, non_blocking=True)
                crop_labels = batch['crop_label'].to(self.device, non_blocking=True)
                disease_labels = batch['disease_label'].to(self.device, non_blocking=True)
                severities = batch['severity'].to(self.device, non_blocking=True)
                
                with torch.amp.autocast('cuda' if self.device == "cuda" else "cpu"):
                    outputs = self.model(images)
                    loss_crop = self.criterion_crop(outputs['crop_logits'], crop_labels)
                    loss_disease = self.criterion_disease(outputs['disease_logits'], disease_labels)
                    loss_severity = self.criterion_severity(outputs['severity'].squeeze(), severities)
                
                val_loss += (loss_crop + loss_disease + loss_severity).item()
                
                _, d_preds = torch.max(outputs['disease_logits'], 1)
                all_d_labels.extend(disease_labels.cpu().numpy())
                all_d_preds.extend(d_preds.cpu().numpy())
        
        acc = accuracy_score(all_d_labels, all_d_preds)
        precision, recall, f1, _ = precision_recall_fscore_support(all_d_labels, all_d_preds, average='weighted', zero_division=0)
        
        return {
            "val_loss": val_loss / len(self.val_loader),
            "accuracy": acc,
            "f1": f1,
            "precision": precision,
            "recall": recall
        }

    def run(self, num_epochs=25):
        script_dir = os.path.dirname(__file__)
        latest_path = os.path.join(script_dir, "latest_checkpoint.pth")
        best_path = os.path.join(script_dir, "agrinet_v5_best.pth")
        
        start_epoch = 0
        best_f1 = 0
        
        # Load existing checkpoint if possible
        if os.path.exists(latest_path):
            try:
                print(f"Loading checkpoint: {latest_path}")
                checkpoint = torch.load(latest_path, map_location=self.device)
                self.model.load_state_dict(checkpoint['model_state_dict'])
                self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
                if 'scheduler_state_dict' in checkpoint:
                    self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
                start_epoch = checkpoint['epoch'] + 1
                best_f1 = checkpoint.get('best_f1', 0)
                print(f"Resumed from epoch {start_epoch}. Best F1: {best_f1:.4f}")
            except Exception as e:
                print(f"Resume failed: {e}")

        print(f"Starting Optimized Training on {self.device}...")
        
        for epoch in range(start_epoch, num_epochs):
            start_time = time.time()
            train_loss = self.train_epoch(epoch)
            metrics = self.evaluate()
            
            epoch_time = (time.time() - start_time) / 60
            
            print(f"\nEpoch {epoch+1}/{num_epochs} Summary ({epoch_time:.2f} min):")
            print(f"  Train Loss: {train_loss:.4f} | Val Loss: {metrics['val_loss']:.4f}")
            print(f"  Accuracy: {metrics['accuracy']:.4f} | F1: {metrics['f1']:.4f}")
            
            # Save latest
            torch.save({
                'epoch': epoch,
                'model_state_dict': self.model.state_dict(),
                'optimizer_state_dict': self.optimizer.state_dict(),
                'scheduler_state_dict': self.scheduler.state_dict(),
                'best_f1': max(best_f1, metrics['f1'])
            }, latest_path)
            
            # Save best
            if metrics['f1'] > best_f1:
                best_f1 = metrics['f1']
                torch.save(self.model.state_dict(), best_path)
                print(f"  *** New Best F1 Score: {best_f1:.4f} - Saved Model ***")
            
            # Early stopping check
            self.early_stopping(metrics['f1'])
            if self.early_stopping.early_stop:
                print("Early stopping triggered. Training stopped.")
                break

if __name__ == "__main__":
    # Config
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(script_dir))))
    dataset_root = os.path.join(project_root, "backend", "dataset_unified")
    
    with open(os.path.join(data_dir, 'crop_map.json'), 'r') as f:
        crop_map = json.load(f)
    with open(os.path.join(data_dir, 'disease_map.json'), 'r') as f:
        disease_map = json.load(f)
        
    # Dataframes
    train_df = pd.read_csv(os.path.join(data_dir, 'train.csv'))
    val_df = pd.read_csv(os.path.join(data_dir, 'val.csv'))
    train_df['image_path'] = train_df['image_path'].apply(lambda x: os.path.join(dataset_root, x))
    val_df['image_path'] = val_df['image_path'].apply(lambda x: os.path.join(dataset_root, x))
    
    # Speed Optimization: Reduce image size for faster training on 4GB GPU
    # Most plant disease models work great at 256x256
    img_size = 256 
    
    train_ds = AgriDatasetV5(
        image_paths=train_df['image_path'].tolist(),
        crop_labels=train_df['crop_id'].tolist(),
        disease_labels=train_df['disease_id'].tolist(),
        severities=train_df['severity'].tolist(),
        transform=get_v5_train_transforms(img_size=img_size)
    )
    
    val_ds = AgriDatasetV5(
        image_paths=val_df['image_path'].tolist(),
        crop_labels=val_df['crop_id'].tolist(),
        disease_labels=val_df['disease_id'].tolist(),
        severities=val_df['severity'].tolist(),
        transform=get_v5_val_transforms(img_size=img_size)
    )
    
    # DataLoader Tuning for 4GB RTX 3050 Laptop
    # Increase num_workers and use pin_memory
    train_loader = DataLoader(
        train_ds, 
        batch_size=32, # Increased batch size
        shuffle=True, 
        num_workers=4, 
        pin_memory=True,
        persistent_workers=True
    )
    
    val_loader = DataLoader(
        val_ds, 
        batch_size=32, 
        shuffle=False, 
        num_workers=4, 
        pin_memory=True,
        persistent_workers=True
    )
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AgriNetV5(num_crops=len(crop_map), num_diseases=len(disease_map), pretrained=True)
    
    trainer = AgriTrainerV5Optimized(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        device=device,
        max_lr=1e-3 # Higher LR with OneCycleLR
    )
    
    trainer.run(num_epochs=25)
