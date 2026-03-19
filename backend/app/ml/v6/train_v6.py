import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import os
import time

from ..v5.model_v5 import AgriNetV5 
from .dataset_v6 import AgriDatasetV6, get_v6_train_transforms, get_v6_val_transforms

class AgriTrainerV6:
    """
    AgroCure AI Trainer v6
    Implements:
    - Unified Dataset Training
    - Early Stopping
    - Learning Rate Scheduling
    - Comprehensive Evaluation (Classification Report + CM)
    """
    def __init__(
        self, 
        model, 
        train_loader, 
        val_loader, 
        device="cuda",
        patience=5
    ):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = device
        self.patience = patience
        
        # Loss & Optimizer
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-4)
        
        # LR Scheduler
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode='max', factor=0.5, patience=2, verbose=True
        )
        
        self.scaler = torch.amp.GradScaler('cuda') if device == "cuda" else None

    def train_epoch(self):
        self.model.train()
        total_loss = 0
        pbar = tqdm(self.train_loader, desc="Training")
        
        for batch in pbar:
            images = batch['image'].to(self.device)
            labels = batch['disease_label'].to(self.device)
            
            self.optimizer.zero_grad()
            
            with torch.amp.autocast('cuda' if self.device == "cuda" else "cpu"):
                outputs = self.model(images)
                loss = self.criterion(outputs['disease_logits'], labels)
            
            if self.scaler:
                self.scaler.scale(loss).backward()
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                loss.backward()
                self.optimizer.step()
                
            total_loss += loss.item()
            pbar.set_postfix({'loss': f'{loss.item():.4f}'})
            
        return total_loss / len(self.train_loader)

    def evaluate(self):
        self.model.eval()
        all_labels = []
        all_preds = []
        
        with torch.no_grad():
            for batch in self.val_loader:
                images = batch['image'].to(self.device)
                labels = batch['disease_label'].to(self.device)
                
                outputs = self.model(images)
                _, preds = torch.max(outputs['disease_logits'], 1)
                
                all_labels.extend(labels.cpu().numpy())
                all_preds.extend(preds.cpu().numpy())
        
        report = classification_report(all_labels, all_preds, output_dict=True, zero_division=0)
        cm = confusion_matrix(all_labels, all_preds)
        
        return report['weighted avg']['f1-score'], report, cm

    def run(self, num_epochs=50):
        print(f"Starting V6 Multi-Dataset Training on {self.device}...")
        best_f1 = 0
        epochs_no_improve = 0
        
        for epoch in range(num_epochs):
            train_loss = self.train_epoch()
            f1, report, cm = self.evaluate()
            
            # Step Scheduler
            self.scheduler.step(f1)
            
            print(f"Epoch {epoch+1}/{num_epochs}:")
            print(f"  Train Loss: {train_loss:.4f} | Val F1: {f1:.4f}")
            
            # Save Best Model
            if f1 > best_f1:
                best_f1 = f1
                torch.save(self.model.state_dict(), "agrinet_v6_best.pth")
                print(f"  [Model Saved] New Best F1: {f1:.4f}")
                epochs_no_improve = 0
            else:
                epochs_no_improve += 1
                
            # Early Stopping
            if epochs_no_improve >= self.patience:
                print(f"Early stopping triggered after {epoch+1} epochs.")
                break
                
        # Final Evaluation Report
        print("\nFinal Training Report:")
        print(f"Best Validation F1: {best_f1:.4f}")
        return report, cm

if __name__ == "__main__":
    # In practice, this would be invoked after Data Integration
    pass
