import requests
import json
import os

def test_e2e_api():
    base_url = "http://localhost:8000/api/v1/disease-ai/analyze"
    
    print("--- Final E2E API Verification ---")
    
    # 1. Prepare Test Data
    # Assuming there's a test image in the backend folder
    img_path = "test_image.jpg"
    if not os.path.exists(img_path):
        # Create a dummy image if not exists
        with open(img_path, "wb") as f:
            f.write(b"dummy_image_data_agrocure_ai_test")
    
    files = {
        "image": ("test_image.jpg", open(img_path, "rb"), "image/jpeg")
    }
    
    data = {
        "crop_name": "Tomato",
        "lat": 19.0760,
        "lon": 72.8777,
        "soil_ph": 6.2,
        "soil_n": 15.0,
        "soil_p": 10.0,
        "soil_k": 10.0,
        "language": "en"
    }

    # 2. Call API
    print(f"Calling endpoint: {base_url}")
    print(f"Payload: {data}")
    
    try:
        response = requests.post(base_url, files=files, data=data)
        response.raise_for_status()
        result = response.json()
        
        # 3. Verify Response Structure
        print("\nAPI Response Structure Check:")
        keys_to_check = [
            "disease_name", 
            "severity", 
            "environmental_risk", 
            "soil_analysis", 
            "llm_reasoning",
            "chemical_treatment",
            "organic_treatment"
        ]
        
        success = True
        for key in keys_to_check:
            if key in result:
                print(f" [OK] Found key: {key}")
            else:
                print(f" [FAIL] Missing key: {key}")
                success = False
        
        if success:
            print("\nE2E API Verification: SUCCESS")
            print(f"Detected: {result.get('disease_name')}")
            
            env_risk = result.get('environmental_risk') or {}
            print(f"Environmental Risk: {env_risk.get('risk_level')}")
            
            soil_ans = result.get('soil_analysis') or {}
            print(f"Soil Status: {len(soil_ans.get('deficiencies', []))} deficiencies found")
            
            llm_reason = result.get('llm_reasoning') or {}
            explanation = llm_reason.get('explanation', 'N/A')
            print(f"AI Reasoning: {explanation[:100]}...")
        else:
            print("\nE2E API Verification: PARTIAL FAILURE")
            
    except Exception as e:
        print(f"\nE2E API Verification: FAILED - {str(e)}")

if __name__ == "__main__":
    test_e2e_api()
