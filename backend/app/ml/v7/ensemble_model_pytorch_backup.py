import torch
import torch.nn as nn
import timm

class AgriEnsembleV7(nn.Module):
    """
    AgroCure AI Ensemble v7
    Combines:
    - EfficientNet-B0 (Texture & Detail)
    - MobileNetV3-Small (Speed & Lightweight)
    
    Targeting 4 classes: Healthy, Blight, Powdery Mildew, Leaf Spot
    """
    def __init__(self, num_classes=4, pretrained=True):
        super(AgriEnsembleV7, self).__init__()
        
        # 1. EfficientNet-B0
        self.effnet = timm.create_model(
            'efficientnet_b0', 
            pretrained=pretrained, 
            num_classes=num_classes
        )
        
        # 2. MobileNetV3-Small
        self.mobilenet = timm.create_model(
            'mobilenetv3_small_100', 
            pretrained=pretrained, 
            num_classes=num_classes
        )

    def forward(self, x):
        # In training, we return both for individual losses
        # In inference, we'll average them
        out_eff = self.effnet(x)
        out_mobile = self.mobilenet(x)
        
        return {
            "eff_logits": out_eff,
            "mobile_logits": out_mobile
        }

if __name__ == "__main__":
    model = AgriEnsembleV7(num_classes=4, pretrained=False)
    x = torch.randn(1, 3, 224, 224)
    out = model(x)
    print(f"EffNet shape: {out['eff_logits'].shape}")
    print(f"MobileNet shape: {out['mobile_logits'].shape}")
    print("Ensemble model v7 initialized successfully.")
