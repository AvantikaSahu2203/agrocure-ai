import torch
import torch.nn as nn
import timm
from typing import Dict, Optional

class AgriNetX(nn.Module):
    """
    AgriNet-X: Hybrid Swin Transformer + Multimodal Fusion.
    - Backbone: Swin-V2 Base (Pre-trained on ImageNet-22K)
    - Multimodal: Image Features + Weather + Soil
    - Heads: Crop (Classification), Binary (Gatekeeper), Disease (Expert), Severity (Regression)
    """
    def __init__(
        self, 
        num_crop_classes: int, 
        num_disease_classes: int,
        weather_dim: int = 3, # [temp, humidity, rainfall]
        soil_dim: int = 4     # [pH, N, P, K]
    ):
        super(AgriNetX, self).__init__()
        
        # 1. Swin Base Backbone from Hugging Face (via timm)
        # Using 384x384 window-12 variant for superior disease localization
        self.backbone = timm.create_model(
            'swin_base_patch4_window12_384', 
            pretrained=True, 
            num_classes=0
        )
        
        # Swin-V2 Base has 1024 output features
        self.feature_dim = self.backbone.num_features
        
        # 2. Multimodal Fusion Layer
        # Concatenate 1024 (Image) + 3 (Weather) + 4 (Soil) = 1031
        self.fusion_dim = self.feature_dim + weather_dim + soil_dim
        
        # Shared bottleneck
        self.bottleneck = nn.Sequential(
            nn.Linear(self.fusion_dim, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.3)
        )
        
        # 3. Prediction Heads
        self.crop_head = nn.Linear(512, num_crop_classes)
        
        # CRITICAL FIX: Two-Stage Classification (Objective 1)
        # Stage 1: Binary [Healthy vs Diseased]
        self.binary_head = nn.Sequential(
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Linear(128, 1) # Output raw logit for BCEWithLogitsLoss
        )
        
        # Stage 2: Multi-class Disease Expert
        self.disease_head = nn.Linear(512, num_disease_classes)
        
        self.severity_head = nn.Sequential(
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid() # Severity as 0-1 percentage
        )

    def forward(self, x: torch.Tensor, weather: torch.Tensor, soil: torch.Tensor) -> Dict[str, torch.Tensor]:
        # Image Features
        features = self.backbone(x) # [batch, 768]
        
        # Fusion
        combined = torch.cat([features, weather, soil], dim=1)
        
        # Bottleneck
        shared_out = self.bottleneck(combined)
        
        # Outputs
        return {
            'crop': self.crop_head(shared_out),
            'binary': self.binary_head(shared_out).squeeze(-1),
            'disease': self.disease_head(shared_out),
            'severity': self.severity_head(shared_out).squeeze(-1)
        }

if __name__ == "__main__":
    # Test model initialization
    model = AgriNetX(num_crop_classes=10, num_disease_classes=38)
    print(f"AgriNet-X Initialized.")
    
    # Mock input
    img = torch.randn(1, 3, 512, 512)
    weather = torch.randn(1, 3)
    soil = torch.randn(1, 4)
    
    out = model(img, weather, soil)
    print(f"Outputs: {out.keys()}")
    print(f"Disease shape: {out['disease'].shape}")
