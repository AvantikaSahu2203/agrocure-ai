import sys
import os
import hashlib
from typing import Dict

# Mock the environment to load backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app.services.ai_analyzer import ai_analyzer, DISEASE_DATABASE

def test_deterministic_detection():
    print("--- Testing Deterministic Detection ---")
    crop = "mango"
    image_data = b"fake_leaf_image_mango_123"
    
    # Run analysis twice with same image
    res1 = ai_analyzer.analyze_image(crop, image_data)
    res2 = ai_analyzer.analyze_image(crop, image_data)
    
    # Verify consistency
    if res1["disease_name"] == res2["disease_name"] and res1["confidence"] == res2["confidence"]:
        print(f"PASS: Deterministic results for {crop} (Result: {res1['disease_name']})")
    else:
        print(f"FAIL: Inconsistent results for {crop}")
        print(f"  Attempt 1: {res1['disease_name']} ({res1['confidence']})")
        print(f"  Attempt 2: {res2['disease_name']} ({res2['confidence']})")

def test_expanded_database():
    print("\n--- Testing Expanded Database ---")
    crops_to_test = ["mango", "cotton", "tomato"]
    
    for crop in crops_to_test:
        image_data = f"sample_image_{crop}_data".encode()
        res = ai_analyzer.analyze_image(crop, image_data)
        
        print(f"Crop: {crop.capitalize()}")
        print(f"  Disease: {res['disease_name']}")
        print(f"  Chemical: {res['chemical_treatment']}")
        print(f"  Organic: {res['organic_treatment']}")
        print(f"  Dosage: {res['dosage']}")
        
        if "Consult" not in res['chemical_treatment'] and len(res['recommendations']) > 0:
            print(f"  PASS: Detailed data found for {crop}")
        else:
            print(f"  WARNING: Generic data returned for {crop}")

def test_translation_quality():
    print("\n--- Testing Multilingual Quality ---")
    crop = "tomato"
    image_data = b"tomato_leaf_test"
    
    # Test Hindi
    res_hi = ai_analyzer.analyze_image(crop, image_data, language="hi")
    print(f"Hindi Analysis: {res_hi['analysis'][:100]}...")
    
    if "छवि विश्लेषण के आधार पर" in res_hi['analysis']:
        print("  PASS: Hindi template reconstruction successful")
    else:
        print("  FAIL: Hindi translation missing or incorrect")

if __name__ == "__main__":
    test_deterministic_detection()
    test_expanded_database()
    test_translation_quality()
