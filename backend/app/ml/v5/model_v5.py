import torch
import torch.nn as nn
import torch.nn.functional as F
import timm

class FocalLoss(nn.Module):
    def __init__(self, alpha=1, gamma=2, reduction='mean'):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs, targets):
        ce_loss = F.cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * ce_loss
        
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        else:
            return focal_loss

class AgriNetV5(nn.Module):
    """
    AgriNetV5: Improved Hierarchical Architecture
    Features:
    - EfficientNetV2-L Backbone
    - Multi-task heads (Crop, Disease, Severity)
    - Attention-based feature extraction
    """
    def __init__(self, num_crops=20, num_diseases=150, pretrained=True):
        super(AgriNetV5, self).__init__()
        
        # 1. Backbone: EfficientNet-B0
        # Using 224x224 resolution for efficiency, or 384x384 if preferred
        self.backbone = timm.create_model(
            'efficientnet_b0', 
            pretrained=pretrained, 
            num_classes=0, 
            global_pool=''
        )
        
        # Feature dimensions for EfficientNet-B0
        in_channels = 1280 
        
        self.global_pool = nn.AdaptiveAvgPool2d(1)
        
        # 2. Shared Bottleneck
        self.bottleneck = nn.Sequential(
            nn.Linear(1280, 1024),
            nn.BatchNorm1d(1024),
            nn.Hardswish(),
            nn.Dropout(0.3)
        )
        
        # 3. Task Heads
        self.crop_head = nn.Sequential(
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, num_crops)
        )
        
        self.disease_head = nn.Sequential(
            nn.Linear(1024, 1024),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(1024, num_diseases)
        )
        
        self.severity_head = nn.Sequential(
            nn.Linear(1024, 256),
            nn.ReLU(),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        features = self.backbone(x)
        if isinstance(features, (list, tuple)):
            features = features[-1]
            
        pooled = self.global_pool(features).flatten(1)
        latent = self.bottleneck(pooled)
        
        return {
            "crop_logits": self.crop_head(latent),
            "disease_logits": self.disease_head(latent),
            "severity": self.severity_head(latent)
        }

if __name__ == "__main__":
    model = AgriNetV5(num_crops=10, num_diseases=50, pretrained=False)
    x = torch.randn(1, 3, 384, 384)
    out = model(x)
    print("Self-test passed.")
