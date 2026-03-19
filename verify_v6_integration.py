import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.ml.model import disease_model
from app.agents.disease_agent import DiseaseDetectionAgent

def test_integration():
    print("--- Starting Integration Test ---")
    
    # 1. Check if model is loaded (should be mock or legacy since we didn't train v6 weights yet)
    print(f"Is v6 engine loaded? {disease_model.v6_engine is not None}")
    
    # 2. Test predict directly
    mock_image = b"fake_image_data"
    pred = disease_model.predict(mock_image, "Tomato")
    print(f"Prediction result: {pred}")
    
    # 3. Test Agent execute
    agent = DiseaseDetectionAgent()
    input_data = {
        "image": mock_image,
        "crop_name": "Tomato",
        "leaf_color": "Yellow"
    }
    result = agent.execute(input_data)
    print(f"Agent result: {result['disease_name']} (Confidence: {result['confidence']})")
    print(f"Severity: {result['severity']}")
    print(f"Color Inference: {result['color_inference']}")
    
    print("--- Test Complete ---")

if __name__ == "__main__":
    test_integration()
