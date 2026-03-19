import torch
import torch.nn as nn
import torch.nn.functional as F
import timm
from typing import Dict, Tuple

class ChannelAttention(nn.Module):
    def __init__(self, in_planes, ratio=16):
        super(ChannelAttention, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        
        self.fc = nn.Sequential(
            nn.Conv2d(in_planes, in_planes // ratio, 1, bias=False),
            nn.ReLU(),
            nn.Conv2d(in_planes // ratio, in_planes, 1, bias=False)
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = self.fc(self.avg_pool(x))
        max_out = self.fc(self.max_pool(x))
        out = avg_out + max_out
        return self.sigmoid(out)

class SpatialAttention(nn.Module):
    def __init__(self, kernel_size=7):
        super(SpatialAttention, self).__init__()
        self.conv1 = nn.Conv2d(2, 1, kernel_size, padding=kernel_size//2, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        x = torch.cat([avg_out, max_out], dim=1)
        x = self.conv1(x)
        return self.sigmoid(x)

class CBAM(nn.Module):
    def __init__(self, in_planes, ratio=16, kernel_size=7):
        super(CBAM, self).__init__()
        self.ca = ChannelAttention(in_planes, ratio)
        self.sa = SpatialAttention(kernel_size)

    def forward(self, x):
        out = self.ca(x) * x
        out = self.sa(out) * out
        return out

class AgriSOTANet(nn.Module):
    def __init__(self, num_classes: int = 38, pretrained: bool = True):
        super(AgriSOTANet, self).__init__()
        
        # 1. Backbone: EfficientNetV2-Medium
        self.backbone = timm.create_model('efficientnetv2_m', pretrained=pretrained, features_only=True)
        # Extract features from the last stage (usually stage 4 or 5)
        # For effnetv2_m, stage 4 output is 1280 channels (typically)
        feature_info = self.backbone.feature_info[-1]
        in_channels = feature_info['num_chs']
        
        # 2. Attention: CBAM
        self.attention = CBAM(in_channels)
        
        # 3. Vision Transformer Head
        self.d_model = 512
        self.projection = nn.Conv2d(in_channels, self.d_model, kernel_size=1)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.d_model, 
            nhead=8, 
            dim_feedforward=2048, 
            dropout=0.1, 
            activation='gelu',
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=4)
        
        # 4. Multi-Task Heads
        self.cls_head = nn.Sequential(
            nn.Linear(self.d_model, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, num_classes)
        )
        
        self.sev_head = nn.Sequential(
            nn.Linear(self.d_model, 256),
            nn.ReLU(),
            nn.Linear(256, 1),
            nn.Sigmoid() # Severity as 0-1 percentage
        )

    def forward(self, x):
        # Backbone Features
        features = self.backbone(x)[-1] # (B, C, H, W)
        
        # Channel & Spatial Attention
        attn_features = self.attention(features)
        
        # Project to Transformer dimension
        projected = self.projection(attn_features) # (B, d_model, H, W)
        B, C, H, W = projected.shape
        
        # Tokenize (Flatten H, W)
        tokens = projected.flatten(2).transpose(1, 2) # (B, H*W, d_model)
        
        # Global Context via Transformer
        transformed = self.transformer_encoder(tokens) # (B, SequencLen, d_model)
        
        # Global Average Pooling of tokens
        global_features = transformed.mean(dim=1) # (B, d_model)
        
        # Multi-Task Outputs
        logits = self.cls_head(global_features)
        severity = self.sev_head(global_features)
        
        return {
            "logits": logits,
            "severity": severity
        }

if __name__ == "__main__":
    # Test Architecture
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AgriSOTANet(num_classes=38).to(device)
    dummy_input = torch.randn(1, 3, 224, 224).to(device)
    output = model(dummy_input)
    print(f"Model Output Shapes - Logits: {output['logits'].shape}, Severity: {output['severity'].shape}")
    
    # Calculate Params
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Total Parameters: {total_params / 1e6:.2f}M")
