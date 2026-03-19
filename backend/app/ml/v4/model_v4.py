import torch
import torch.nn as nn
import timm
from typing import Dict, Optional

class AgriNextNet(nn.Module):
    """
    AgriNextNet (v4 Architecture)
    Hierarchical multi-task model for Crop + Disease + Severity.
    """
    def __init__(
        self, 
        num_crops: int = 20, 
        num_diseases: int = 150, 
        pretrained: bool = True
    ):
        super(AgriNextNet, self).__init__()
        
        # 1. Backbone: EfficientNetV2-Large (Robust features)
        # Using 'efficientnetv2_l' for target accuracy of 92-97%
        self.backbone = timm.create_model('efficientnetv2_l', pretrained=pretrained, num_classes=0, global_pool='')
        
        # Get feature dimensions
        feature_info = self.backbone.feature_info[-1]
        in_channels = feature_info['num_chs']
        
        # 2. Local/Global Context Head (Swin Transformer Blocks)
        # For agricultural patterns, spatial relationships are key
        self.global_pool = nn.AdaptiveAvgPool2d(1)
        
        # 3. Hierarchical Prediction Heads
        # Feature bottleneck
        self.bottleneck = nn.Sequential(
            nn.Linear(in_channels, 1024),
            nn.BatchNorm1d(1024),
            nn.GELU(),
            nn.Dropout(0.3)
        )
        
        # Crop Classifier (Plant Type)
        self.crop_head = nn.Sequential(
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, num_crops)
        )
        
        # Disease Classifier (Condition)
        # Conditional feature: we could concatenate crop features here, 
        # but for now, we use a large shared representation.
        self.disease_head = nn.Sequential(
            nn.Linear(1024, 1024),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(1024, num_diseases)
        )
        
        # Severity Regressor
        self.severity_head = nn.Sequential(
            nn.Linear(1024, 256),
            nn.ReLU(),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        # Extract features
        features = self.backbone(x)
        if isinstance(features, list):
            features = features[-1]
            
        # Global Pooling
        pooled = self.global_pool(features).flatten(1)
        
        # Bottleneck
        latent = self.bottleneck(pooled)
        
        # Outputs
        crop_logits = self.crop_head(latent)
        disease_logits = self.disease_head(latent)
        severity = self.severity_head(latent)
        
        return {
            "crop_logits": crop_logits,
            "disease_logits": disease_logits,
            "severity": severity
        }

if __name__ == "__main__":
    # Test model
    model = AgriNextNet(num_crops=15, num_diseases=50, pretrained=False)
    x = torch.randn(1, 3, 224, 224)
    out = model(x)
    print(f"Crop Logits: {out['crop_logits'].shape}")
    print(f"Disease Logits: {out['disease_logits'].shape}")
    print(f"Severity: {out['severity'].shape}")
