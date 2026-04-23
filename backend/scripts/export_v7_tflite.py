import torch
import torch.nn as nn
import onnx
import os
import sys

# Add backend to path to import models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from app.ml.v7.ensemble_model import AgriEnsembleV7
except ImportError:
    # Fallback if imports are tricky
    import timm
    class AgriEnsembleV7(nn.Module):
        def __init__(self, num_classes=4):
            super(AgriEnsembleV7, self).__init__()
            self.effnet = timm.create_model('efficientnet_b0', pretrained=False, num_classes=num_classes)
            self.mobilenet = timm.create_model('mobilenetv3_small_100', pretrained=False, num_classes=num_classes)
        def forward(self, x):
            # Average the ensemble for inference
            out_eff = self.effnet(x)
            out_mobile = self.mobilenet(x)
            return (out_eff + out_mobile) / 2

def export_v7_to_tflite(weights_path, output_tflite="crop_model_v7.tflite"):
    print(f"Loading weights from {weights_path}...")
    model = AgriEnsembleV7(num_classes=4)
    if os.path.exists(weights_path):
        model.load_state_dict(torch.load(weights_path, map_location='cpu'))
    model.eval()

    # 1. Export to ONNX
    # Important: Use batch_size=1
    dummy_input = torch.randn(1, 3, 128, 128) 
    onnx_path = "crop_model_v7.onnx"
    
    print("Exporting to ONNX (Batch Size = 1)...")
    torch.onnx.export(
        model,
        dummy_input,
        onnx_path,
        export_params=True,
        opset_version=12,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        # Disable dynamic axes to force batch_size=1 if needed, 
        # but usually 1 is the default from dummy_input
    )

    print(f"ONNX model saved to {onnx_path}")
    print("\nNext Steps:")
    print("1. Install onnx2tf: pip install onnx2tf")
    print(f"2. Convert to TFLite: onnx2tf -i {onnx_path} -o {output_tflite}")
    print("3. Move the new .tflite to your mobile app assets/models/ folder.")

if __name__ == "__main__":
    weights = "agrinet_ensemble_v7_best.pth"
    if not os.path.exists(weights):
        # Check current dir
        weights = "../agrinet_ensemble_v7_best.pth"
        
    export_v7_to_tflite(weights)
