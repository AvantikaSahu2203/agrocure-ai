import torch
import torch.nn as nn
import timm
from PIL import Image
import torchvision.transforms as T
import os

# 1. Model Architecture
class AgriEnsembleV7(nn.Module):
    def __init__(self, num_classes=4):
        super(AgriEnsembleV7, self).__init__()
        self.effnet = timm.create_model('efficientnet_b0', pretrained=False, num_classes=num_classes)
        self.mobilenet = timm.create_model('mobilenetv3_small_100', pretrained=False, num_classes=num_classes)
    def forward(self, x):
        return {"eff_logits": self.effnet(x), "mobile_logits": self.mobilenet(x)}

# 2. Inference Class
class StandaloneInferenceV7:
    def __init__(self, weights_path):
        self.device = torch.device("cpu")
        self.model = AgriEnsembleV7(num_classes=4).to(self.device)
        self.model.load_state_dict(torch.load(weights_path, map_location=self.device))
        self.model.eval()
        
        # Using standard torchvision transforms to avoid pydantic issues
        self.transform = T.Compose([
            T.Resize((224, 224)),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        self.classes = ["Healthy", "Blight", "Powdery Mildew", "Leaf Spot"]

    @torch.no_grad()
    def predict(self, image_path):
        image = Image.open(image_path).convert('RGB')
        input_tensor = self.transform(image).unsqueeze(0)
        outputs = self.model(input_tensor)
        avg_logits = (outputs['eff_logits'] + outputs['mobile_logits']) / 2
        probs = torch.softmax(avg_logits, dim=1)
        conf, idx = torch.max(probs, 1)
        return self.classes[idx.item()], float(conf.item())

# 3. Execution
if __name__ == "__main__":
    weights = r"C:\Users\ASUS\Desktop\AgroCure AI\backend\agrinet_ensemble_v7_best.pth"
    img = r"C:\Users\ASUS\Desktop\AgroCure AI\backend\test_image.jpg"
    
    print("\n--- STANDALONE V7 LAPTOP VERIFICATION ---")
    if not os.path.exists(weights):
        print(f"Error: Weights not found at {weights}")
    elif not os.path.exists(img):
        print(f"Error: Image not found at {img}")
    else:
        engine = StandaloneInferenceV7(weights)
        label, confidence = engine.predict(img)
        print(f"RESULT: {label}")
        print(f"CONFIDENCE: {confidence*100:.2f}%")
        print("\nSUCCESS: V7 Ensemble is working nicely on your laptop!")
