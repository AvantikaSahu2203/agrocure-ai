import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm
import numpy as np
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, confusion_matrix
import os

from .model_v5 import AgriNetV5, FocalLoss
from .dataset_v5 import AgriDatasetV5, get_v5_train_transforms, get_v5_val_transforms

class AgriTrainerV5:
    def __init__(
        self, 
        model, 
        train_loader, 
        val_loader, 
        device="cuda",
        class_weights=None
    ):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = device
        
        # 1. Losses
        # Focal Loss for disease classification to handle imbalances
        self.criterion_disease = FocalLoss(alpha=1, gamma=2)
        # standard CE for crop type
        self.criterion_crop = nn.CrossEntropyLoss(weight=class_weights)
        # MSE for severity
        self.criterion_severity = nn.MSELoss()
        
        # 2. Optimizer & Scheduler
        self.optimizer = optim.AdamW(self.model.parameters(), lr=1e-4, weight_decay=1e-2)
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(self.optimizer, mode='min', factor=0.5, patience=2)
        
        self.scaler = torch.amp.GradScaler('cuda') if device == "cuda" else None

    def train_epoch(self):
        self.model.train()
        total_loss = 0
        pbar = tqdm(self.train_loader, desc="Training")
        
        for batch in pbar:
            images = batch['image'].to(self.device)
            crop_labels = batch['crop_label'].to(self.device)
            disease_labels = batch['disease_label'].to(self.device)
            severities = batch['severity'].to(self.device)
            
            self.optimizer.zero_grad()
            
            with torch.amp.autocast('cuda' if self.device == "cuda" else "cpu"):
                outputs = self.model(images)
                loss_crop = self.criterion_crop(outputs['crop_logits'], crop_labels)
                loss_disease = self.criterion_disease(outputs['disease_logits'], disease_labels)
                loss_severity = self.criterion_severity(outputs['severity'].squeeze(), severities)
                
                # Combined Loss
                loss = loss_crop + 2.0 * loss_disease + 0.5 * loss_severity
            
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
        all_d_labels = []
        all_d_preds = []
        val_loss = 0
        
        with torch.no_grad():
            for batch in self.val_loader:
                images = batch['image'].to(self.device)
                crop_labels = batch['crop_label'].to(self.device)
                disease_labels = batch['disease_label'].to(self.device)
                severities = batch['severity'].to(self.device)
                
                outputs = self.model(images)
                loss_crop = self.criterion_crop(outputs['crop_logits'], crop_labels)
                loss_disease = self.criterion_disease(outputs['disease_logits'], disease_labels)
                loss_severity = self.criterion_severity(outputs['severity'].squeeze(), severities)
                
                val_loss += (loss_crop + loss_disease + loss_severity).item()
                
                _, d_preds = torch.max(outputs['disease_logits'], 1)
                all_d_labels.extend(disease_labels.cpu().numpy())
                all_d_preds.extend(d_preds.cpu().numpy())
                
        # Metrics reporting
        acc = accuracy_score(all_d_labels, all_d_preds)
        precision, recall, f1, _ = precision_recall_fscore_support(all_d_labels, all_d_preds, average='weighted')
        cm = confusion_matrix(all_d_labels, all_d_preds)
        
        return {
            "val_loss": val_loss / len(self.val_loader),
            "accuracy": acc,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "confusion_matrix": cm
        }

    def run(self, num_epochs=10):
        # Paths
        script_dir = os.path.dirname(__file__)
        latest_path = os.path.join(script_dir, "latest_checkpoint.pth")
        best_path = os.path.join(script_dir, "agrinet_v5_best.pth")
        
        start_epoch = 0
        best_f1 = 0
        
        # Auto-resume logic
        if os.path.exists(latest_path):
            try:
                print(f"Loading latest checkpoint: {latest_path}")
                checkpoint = torch.load(latest_path, map_location=self.device)
                self.model.load_state_dict(checkpoint['model_state_dict'])
                self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
                if 'scheduler_state_dict' in checkpoint and self.scheduler:
                    self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
                start_epoch = checkpoint['epoch'] + 1
                best_f1 = checkpoint.get('best_f1', 0)
                print(f"Successfully resumed from epoch {start_epoch}. Best F1 so far: {best_f1:.4f}")
            except Exception as e:
                print(f"Could not resume from latest checkpoint: {e}")
        elif os.path.exists(best_path):
            try:
                print(f"Loading best model weights: {best_path}")
                checkpoint = torch.load(best_path, map_location=self.device)
                # Handle both full checkpoints and state_dicts
                if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                    self.model.load_state_dict(checkpoint['model_state_dict'])
                else:
                    self.model.load_state_dict(checkpoint)
                print("Successfully loaded best weights.")
                # Evaluate once to get a baseline best_f1
                metrics = self.evaluate()
                best_f1 = metrics['f1']
                print(f"Current Best F1: {best_f1:.4f}")
            except Exception as e:
                print(f"Could not load best weights: {e}")

        print(f"Starting V5 Training on {self.device} from epoch {start_epoch+1}...")
        
        for epoch in range(start_epoch, num_epochs):
            train_loss = self.train_epoch()
            metrics = self.evaluate()
            self.scheduler.step(metrics['val_loss'])
            
            print(f"Epoch {epoch+1}/{num_epochs}:")
            print(f"  Train Loss: {train_loss:.4f} | Val Loss: {metrics['val_loss']:.4f}")
            print(f"  Accuracy: {metrics['accuracy']:.4f} | F1: {metrics['f1']:.4f}")
            print(f"  Precision: {metrics['precision']:.4f} | Recall: {metrics['recall']:.4f}")
            
            # Save latest checkpoint
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': self.model.state_dict(),
                'optimizer_state_dict': self.optimizer.state_dict(),
                'scheduler_state_dict': self.scheduler.state_dict() if self.scheduler else None,
                'best_f1': max(best_f1, metrics['f1']),
                'metrics': metrics
            }
            torch.save(checkpoint, latest_path)
            
            if metrics['f1'] > best_f1:
                best_f1 = metrics['f1']
                # Save just the state dict for inference convenience, 
                # or the full checkpoint for best model
                torch.save(self.model.state_dict(), best_path)
                print(f"Epoch {epoch+1} New Best F1! Saved: {best_path}")

if __name__ == "__main__":
    import pandas as pd
    import json
    
    # 1. Load configuration
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    # Dataset root is in backend/dataset_unified, which is 3 levels up from this script or in the project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(script_dir))))
    dataset_root = os.path.join(project_root, "backend", "dataset_unified")
    
    with open(os.path.join(data_dir, 'crop_map.json'), 'r') as f:
        crop_map = json.load(f)
    with open(os.path.join(data_dir, 'disease_map.json'), 'r') as f:
        disease_map = json.load(f)
        
    num_crops = len(crop_map)
    num_diseases = len(disease_map)
    
    # 2. Load Dataframes
    train_df = pd.read_csv(os.path.join(data_dir, 'train.csv'))
    val_df = pd.read_csv(os.path.join(data_dir, 'val.csv'))
    
    # Prepend dataset root to image paths
    train_df['image_path'] = train_df['image_path'].apply(lambda x: os.path.join(dataset_root, x))
    val_df['image_path'] = val_df['image_path'].apply(lambda x: os.path.join(dataset_root, x))
    
    # 3. Create Datasets & Loaders
    train_ds = AgriDatasetV5(
        image_paths=train_df['image_path'].tolist(),
        crop_labels=train_df['crop_id'].tolist(),
        disease_labels=train_df['disease_id'].tolist(),
        severities=train_df['severity'].tolist(),
        transform=get_v5_train_transforms()
    )
    
    val_ds = AgriDatasetV5(
        image_paths=val_df['image_path'].tolist(),
        crop_labels=val_df['crop_id'].tolist(),
        disease_labels=val_df['disease_id'].tolist(),
        severities=val_df['severity'].tolist(),
        transform=get_v5_val_transforms()
    )
    
    train_loader = DataLoader(train_ds, batch_size=16, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=16, shuffle=False, num_workers=0)
    
    # 4. Initialize Model & Trainer
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AgriNetV5(num_crops=num_crops, num_diseases=num_diseases, pretrained=True)
    
    trainer = AgriTrainerV5(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        device=device
    )
    
    # 5. Run Training
    trainer.run(num_epochs=50) # Set to 50 for longer training
