import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttention, self).__init__()
        self.attn = nn.MultiheadAttention(embed_dim=d_model, num_heads=num_heads, batch_first=True)
    
    def forward(self, query, key, value):
        return self.attn(query, key, value)[0]

class TransAgroNet(nn.Module):
    """
    SOTA Hybrid Model: EfficientNet-B4 + Vision Transformer Bridge.
    Architecture:
    1. CNN Backbone (EfficientNet) for local features.
    2. ViT Transformer blocks for global dependencies.
    3. Multi-task Heads (Classification, Severity, Segmentation).
    """
    def __init__(self, num_classes, d_model=512, nhead=8, num_layers=4):
        super(TransAgroNet, self).__init__()
        
        # 1. Feature Extractor (CNN)
        # Using B4 for balanced complexity/accuracy
        backbone = models.efficientnet_b4(pretrained=True)
        self.cnn_features = nn.Sequential(*list(backbone.children())[:-2])
        
        # 2. Linear Projection to Transformer Dimension
        # B4 last feature map has 1792 channels
        self.proj = nn.Conv2d(1792, d_model, kernel_size=1)
        
        # 3. Vision Transformer Bridge
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # 4. Multi-task Heads
        
        # Head A: Disease Classification
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool1d(1),
            nn.Flatten(),
            nn.Linear(d_model, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )
        
        # Head B: Severity Estimation (Regression)
        self.severity_regressor = nn.Sequential(
            nn.AdaptiveAvgPool1d(1),
            nn.Flatten(),
            nn.Linear(d_model, 256),
            nn.ReLU(),
            nn.Linear(256, 1),
            nn.Sigmoid() # 0 to 1 range for percentage
        )
        
        # Head C: Semantic Segmentation (Leaf Masking)
        # Simplified decoder for production efficiency
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(d_model, 256, kernel_size=4, stride=2, padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(256, 128, kernel_size=4, stride=2, padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1),
            nn.ReLU(),
            nn.Upsample(scale_factor=4, mode='bilinear', align_corners=True), # Match input size
            nn.Conv2d(64, 1, kernel_size=1),
            nn.Sigmoid()
        )

    def forward(self, x):
        # Input shape: (B, 3, 224, 224)
        
        # Local features: (B, 1792, 7, 7)
        local_features = self.cnn_features(x)
        
        # Projected features: (B, d_model, 7, 7)
        feat_map = self.proj(local_features)
        
        # Tokenize (Flatten and transpose): (B, 49, d_model)
        b, c, h, w = feat_map.shape
        tokens = feat_map.flatten(2).transpose(1, 2)
        
        # Global context via Transformer: (B, 49, d_model)
        global_tokens = self.transformer(tokens)
        
        # 1. Classification
        class_logits = self.classifier(global_tokens.transpose(1, 2))
        
        # 2. Severity
        severity_score = self.severity_regressor(global_tokens.transpose(1, 2))
        
        # 3. Segmentation
        # Reshape tokens back to spatial map for decoder
        latent_map = global_tokens.transpose(1, 2).view(b, c, h, w)
        segmentation_mask = self.decoder(latent_map)
        
        return {
            "classification": class_logits,
            "severity": severity_score,
            "segmentation": segmentation_mask
        }

def get_model(num_classes):
    return TransAgroNet(num_classes=num_classes)
