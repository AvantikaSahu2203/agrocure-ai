import sys
import os
import numpy as np

# Add backend to path
sys.path.append(r"c:\Users\ASUS\Desktop\AgroCure AI\backend\app\ml\brinjal")
# Also need to mock some imports if necessary, or just import the class
from brinjal_inference import BrinjalInference

def test_inference():
    print("--- Brinjal Inference Verification ---")
    try:
        bi = BrinjalInference()
        print(f"Model Path: {bi.model_path}")
        print(f"File exists: {os.path.exists(bi.model_path)}")
        
        loaded = bi._load_model()
        print(f"Model Loaded: {loaded}")
        
        if not loaded:
            print(f"ERROR: Model failed to LOAD despite file existence.")
            return
            
        # Create a dummy image (224x224x3)
        dummy_img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        import cv2
        _, img_encoded = cv2.imencode('.jpg', dummy_img)
        img_bytes = img_encoded.tobytes()
        
        result = bi.predict(img_bytes)
        
        print("\n--- Prediction Result ---")
        print(f"Disease: {result['disease_name']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Classes Checked: {len(result['all_probabilities'])}")
        
        expected_classes = [
            "anthracnose",
            "bacterial_wilt",
            "brinjal_healthy",
            "little_leaf",
            "phomopsis_blight",
            "powdery_mildew",
            "verticillium_wilt"
        ]
        
        actual_classes = list(result['all_probabilities'].keys())
        if set(expected_classes) == set(actual_classes):
             print("✅ Class mapping matches notebook exactly.")
        else:
             print(f"❌ Class mapping mismatch! Found: {actual_classes}")

    except Exception as e:
        print(f"Verification Failed: {e}")

if __name__ == "__main__":
    test_inference()
