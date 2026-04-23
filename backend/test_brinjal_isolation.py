import sys
import os
import json
from datetime import datetime

# Setup paths to import from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.agents.disease_agent import DiseaseDetectionAgent

def test_brinjal_routing():
    agent = DiseaseDetectionAgent()
    
    # Mock input data for Brinjal
    input_data = {
        "image": b"fake_image_data",
        "crop_name": "brinjal",
        "leaf_color": "yellow",
        "weather_context": "humid"
    }
    
    print("--- Testing Brinjal Routing ---")
    result = agent.execute(input_data)
    
    print(f"Detected Disease: {result.get('disease_name')}")
    print(f"Is Brinjal Specialized: {result.get('is_brinjal_specialized')}")
    print(f"Scientific Name: {result.get('scientific_name')}")
    
    assert result.get("is_brinjal_specialized") is True
    print("SUCCESS: Brinjal routing confirmed.")

def test_rice_routing():
    agent = DiseaseDetectionAgent()
    
    # Mock input data for Rice
    input_data = {
        "image": b"fake_image_data",
        "crop_name": "rice"
    }
    
    print("\n--- Testing Rice Routing ---")
    result = agent.execute(input_data)
    
    print(f"Detected Disease: {result.get('disease_name')}")
    print(f"Is Rice Specialized: {result.get('is_rice_specialized')}")
    
    assert result.get("is_rice_specialized") is True
    print("SUCCESS: Rice routing confirmed.")

def test_tomato_isolation():
    agent = DiseaseDetectionAgent()
    
    # Mock input data for Tomato (Should NOT use specialized models)
    input_data = {
        "image": b"fake_image_data",
        "crop_name": "tomato"
    }
    
    print("\n--- Testing Tomato Isolation (Ensemble v7) ---")
    result = agent.execute(input_data)
    
    # Standard models don't have these flags
    specialized_brinjal = result.get("is_brinjal_specialized", False)
    specialized_rice = result.get("is_rice_specialized", False)
    
    print(f"Specialized Brinjal: {specialized_brinjal}")
    print(f"Specialized Rice: {specialized_rice}")
    
    assert specialized_brinjal is False
    assert specialized_rice is False
    print("SUCCESS: Ensemble v7 isolation confirmed.")

if __name__ == "__main__":
    try:
        test_brinjal_routing()
        test_rice_routing()
        test_tomato_isolation()
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
