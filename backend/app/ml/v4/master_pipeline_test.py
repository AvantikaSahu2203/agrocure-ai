import os
import sys
import json
from datetime import datetime

# Add project root to sys.path
sys.path.append(os.path.abspath(os.curdir))

from app.services.ai_analyzer import AIPlantAnalyzer

def run_full_pipeline_test():
    print("==========================================")
    print("      AGROCURE AI: FULL PIPELINE TEST     ")
    print("==========================================")

    # 1. Setup
    analyzer = AIPlantAnalyzer()
    
    # Mock data
    crop_name = "Tomato"
    # Using a dummy image (in a real test, this would be a leaf image)
    mock_image = b"fake_image_data_for_testing"
    
    # Contextual data
    lat, lon = 19.0760, 72.8777 # Mumbai
    soil_params = {
        "soil_ph": 5.5,
        "soil_n": 25.0,
        "soil_p": 12.0,
        "soil_k": 20.0
    }
    
    print(f"Step 1: Input Received")
    print(f" - Crop: {crop_name}")
    print(f" - Location: {lat}, {lon}")
    print(f" - Soil: {soil_params}")

    # 2. Execute Full Pipeline
    print(f"\nStep 2: Executing Full Pipeline...")
    result = analyzer.analyze_image(
        crop_name=crop_name,
        image_data=mock_image,
        lat=lat,
        lon=lon,
        **soil_params
    )

    # 3. Analyze Results
    print(f"\nStep 3: Results Received")
    print(f"------------------------------------------")
    print(f"Disease Detected: {result['disease_name']} ({result['scientific_name']})")
    print(f"Confidence: {result['confidence']*100}%")
    print(f"Severity: {result['severity']} ({result['affected_area_percentage']}%)")
    
    print(f"\n[Environmental Risk]")
    env = result.get('environmental_risk', {})
    print(f" - Risk Level: {env.get('risk_level')}")
    print(f" - Probabilty: {env.get('probability')}%")

    print(f"\n[Soil Analysis]")
    soil = result.get('soil_analysis', {})
    print(f" - Deficiencies: {soil.get('deficiencies')}")
    print(f" - Soil Diseases: {soil.get('soil_diseases')}")

    print(f"\n[AI Reasoning (LLM + RAG)]")
    llm = result.get('llm_reasoning', {})
    print(f" - Explanation: {llm.get('explanation')[:150]}...")
    print(f" - Causes: {llm.get('causes')[:150]}...")

    print(f"\n[Treatments & Remedies]")
    print(f" - Chemical: {result['chemical_treatment']}")
    print(f" - Organic: {result['organic_treatment']}")
    
    print(f"\nStep 4: Pipeline Integrity Check")
    required_keys = ['environmental_risk', 'soil_analysis', 'llm_reasoning', 'chemical_treatment']
    missing = [k for k in required_keys if k not in result or not result[k]]
    
    if not missing:
        print("SUCCESS: Full AI Pipeline is fully functional and integrated.")
    else:
        print(f"WARNING: Some pipeline components are missing: {missing}")

if __name__ == "__main__":
    run_full_pipeline_test()
