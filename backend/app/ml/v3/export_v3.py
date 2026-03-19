import torch
import torch.onnx
import os
from .model_v3 import AgriSOTANet

def export_to_onnx(model_path: str, output_path: str = "agrisota.onnx"):
    """
    Exports the trained PyTorch model to ONNX format for efficient inference.
    """
    print(f"Exporting model to {output_path}...")
    
    # Load model
    model = AgriSOTANet(num_classes=38, pretrained=False)
    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    
    # Create dummy input
    dummy_input = torch.randn(1, 3, 224, 224)
    
    # Export
    torch.onnx.export(
        model, 
        dummy_input, 
        output_path,
        export_params=True,
        opset_version=14,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['logits', 'severity'],
        dynamic_axes={'input': {0: 'batch_size'}, 'logits': {0: 'batch_size'}, 'severity': {0: 'batch_size'}}
    )
    print("ONNX Export Complete.")

def convert_to_tflite(onnx_path: str, tflite_path: str = "agrisota.tflite"):
    """
    Placeholder/Utility for TFLite conversion.
    Typically requires `onnx2tf` or `onnx-tensorflow`.
    """
    print(f"To convert {onnx_path} to TFLite, use: onnx2tf -i {onnx_path} -o {tflite_path}")

if __name__ == "__main__":
    # Test Export with untrained model
    model = AgriSOTANet(num_classes=38)
    torch.save(model.state_dict(), "agrisota_temp.pth")
    
    export_to_onnx("agrisota_temp.pth")
    
    # Cleanup
    if os.path.exists("agrisota_temp.pth"):
        os.remove("agrisota_temp.pth")
    # Keep onnx for verification if needed
