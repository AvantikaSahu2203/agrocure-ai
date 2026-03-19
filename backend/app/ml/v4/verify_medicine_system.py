import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.curdir))

from app.services.medicine_service import medicine_service

def test_medicine_system():
    print("--- Medicine Recommendation Verification ---")
    
    # Test case 1: Specific disease (Leaf Spot)
    print("\nTesting: Leaf Spot")
    meds1 = medicine_service.get_recommendation("Leaf Spot")
    print(f"Chemical: {meds1['chemical_medicine']}")
    print(f"Organic: {meds1['organic_remedy']}")
    
    # Test case 2: Variation (Tomato Early Blight)
    print("\nTesting: Tomato Early Blight")
    meds2 = medicine_service.get_recommendation("Tomato Early Blight")
    print(f"Chemical: {meds2['chemical_medicine']}")
    print(f"Organic: {meds2['organic_remedy']}")
    
    # Test case 3: Aphids (Specific chemical requirement check)
    print("\nTesting: Aphids")
    meds3 = medicine_service.get_recommendation("Aphids")
    print(f"Chemical: {meds3['chemical_medicine']}")
    
    # Verification
    if meds1['chemical_medicine'] == "Mancozeb" and meds3['chemical_medicine'] == "Imidacloprid":
        print("\nVerification: SUCCESS")
    else:
        print("\nVerification: CHECK OUTPUTS")

if __name__ == "__main__":
    test_medicine_system()
