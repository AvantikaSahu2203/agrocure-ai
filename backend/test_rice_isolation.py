import sys
import os

# Add backend to path
sys.path.append(r'c:\Users\ASUS\Desktop\AgroCure AI\backend')

from app.agents.disease_agent import DiseaseDetectionAgent

def test_isolation():
    agent = DiseaseDetectionAgent()
    
    print("\n--- Testing Rice Model Branch ---")
    rice_input = {
        "image": b"dummy_image_data",
        "crop_name": "Rice"
    }
    rice_result = agent.execute(rice_input)
    print(f"Rice Accuracy: {rice_result['confidence']*100}%")
    print(f"Disease: {rice_result['disease_name']}")
    print(f"Specialized: {rice_result.get('is_rice_specialized', False)}")
    
    assert rice_result.get('is_rice_specialized') == True
    assert rice_result['disease_name'] in ["Bacterial Blight", "Blast", "Brown Spot"]

    print("\n--- Testing Standard Model Branch (Tomato) ---")
    tomato_input = {
        "image": b"dummy_image_data",
        "crop_name": "Tomato"
    }
    tomato_result = agent.execute(tomato_input)
    # The standard model returns 'is_v6' or 'is_v7' or 'is_mock' (from model.py)
    # We just want to ensure it DOES NOT have 'is_rice_specialized'
    print(f"Tomato Disease: {tomato_result['disease_name']}")
    print(f"Rice Specialized: {tomato_result.get('is_rice_specialized', False)}")
    
    assert tomato_result.get('is_rice_specialized', False) == False

    print("\nTEST PASSED: Isolation verified.")

if __name__ == "__main__":
    try:
        test_isolation()
    except Exception as e:
        print(f"TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
