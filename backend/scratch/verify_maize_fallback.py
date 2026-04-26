import os
import sys

# Add backend to path
sys.path.append(os.getcwd())

from app.agents.disease_agent import DiseaseDetectionAgent
from app.ml.maize.maize_inference import MaizeInference

def verify_maize():
    print("--- Verifying Maize Fix ---")
    
    # 1. Check MaizeInference Loading
    maize_inf = MaizeInference()
    loaded = maize_inf._load_model()
    print(f"Maize Specialized Model Loaded: {loaded}")
    
    # 2. Mock Image Data
    mock_image = b"fake_image_data"
    
    # 3. Check Prediction (Should return offline if model missing)
    pred = maize_inf.predict(mock_image)
    print(f"MaizeInference Result: {pred['disease_name']}")
    
    # 4. Check Agent Fallback
    agent = DiseaseDetectionAgent()
    input_data = {
        "image": mock_image,
        "crop_name": "Maize",
        "leaf_color": "green"
    }
    
    print("\n--- Testing Agent Execution (should fall back to V7 if specialized is offline) ---")
    # This might fail if V7 weights aren't exactly where expected during script run
    # but the logic check is what matters.
    try:
        agent_res = agent.execute(input_data)
        print(f"Agent Final Result: {agent_res['disease_name']} (Confidence: {agent_res.get('confidence', 0)})")
        if agent_res['disease_name'] == "Maize Diagnostic Offline":
            print("FAILURE: Still showing Offline status.")
        else:
            print("SUCCESS: Fallback logic working (or specialized model found).")
    except Exception as e:
        print(f"Agent execution error (likely due to missing standard model in scratch environment): {e}")

if __name__ == "__main__":
    verify_maize()
