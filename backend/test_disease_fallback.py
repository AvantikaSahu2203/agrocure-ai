import sys
import os
import cv2
import numpy as np

# Add current directory to path
sys.path.append(os.getcwd())

from app.services.ai_analyzer import ai_analyzer

def test_white_spot_fallback():
    print("Testing White Spot Fallback for Cucumber...")
    
    # Create a dummy image with white spots (Powdery Mildew simulation)
    # Background: Green (leaf)
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    img[:, :] = [0, 100, 0] # Green
    
    # Add white spots
    for _ in range(50):
        x, y = np.random.randint(0, 400, 2)
        radius = np.random.randint(5, 15)
        cv2.circle(img, (x, y), radius, (255, 255, 255), -1)
    
    # Encode to bytes
    _, buffer = cv2.imencode('.jpg', img)
    image_data = buffer.tobytes()
    
    # Analyze
    result = ai_analyzer.analyze_image(
        crop_name="Cucumber",
        image_data=image_data
    )
    
    print(f"Detected Disease: {result['disease_name']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Symptoms: {result['symptoms_detected']}")
    
    if result['disease_name'] == "Powdery Mildew":
        print("✅ SUCCESS: Fallback correctly identified Powdery Mildew based on white spots.")
    else:
        print("❌ FAILURE: Fallback failed to identify Powdery Mildew.")

if __name__ == "__main__":
    test_white_spot_fallback()
