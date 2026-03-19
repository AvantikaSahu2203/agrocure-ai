import sys
import os
import io

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.services.ai_analyzer import ai_analyzer
import numpy as np
import cv2

def test_v5_uncertainty():
    print("Testing v5 Uncertainty Logic (< 80% confidence)...")
    # Create a dummy image
    dummy_img = np.zeros((384, 384, 3), dtype=np.uint8)
    _, img_encoded = cv2.imencode('.jpg', dummy_img)
    image_data = img_encoded.tobytes()
    
    # We want to force a low confidence or mock state
    # If self.v5_engine is None, it uses mock which has 0.85+ confidence.
    # So we should test if we can mock the engine result if needed, 
    # but let's see what the current implementation does.
    
    result = ai_analyzer.analyze_image(
        crop_name="Tomato",
        image_data=image_data,
        language="en"
    )
    
    print(f"Prediction: {result.get('disease_name')}")
    print(f"Confidence: {result.get('confidence')}")
    print(f"Analysis: {result.get('analysis')}")
    
    if result.get("disease_name") == "Potential Disease – Further Analysis Required":
        print("SUCCESS: Uncertainty logic caught low confidence.")
    else:
        print("INFO: Confidence was high, uncertainty logic not triggered.")

def test_v5_translation():
    print("\nTesting v5 Translation Logic (Hindi)...")
    dummy_img = np.zeros((384, 384, 3), dtype=np.uint8)
    _, img_encoded = cv2.imencode('.jpg', dummy_img)
    image_data = img_encoded.tobytes()
    
    result = ai_analyzer.analyze_image(
        crop_name="Tomato",
        image_data=image_data,
        language="hi"
    )
    
    print(f"Disease (HI): {result.get('disease_name')}")
    print(f"Analysis (HI): {result.get('analysis')[:100]}...")

if __name__ == "__main__":
    try:
        test_v5_uncertainty()
        test_v5_translation()
    except Exception as e:
        print(f"Verification Failed: {e}")
