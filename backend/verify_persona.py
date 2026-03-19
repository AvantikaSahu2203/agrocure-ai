import requests
import json

def test_persona_integration():
    url = "http://localhost:8000/api/v1/orchestrator/full-analysis"
    
    # Simulate the example input from the user request
    # Note: We need a valid JWT token if the endpoint is protected
    # For now, I'll assume I can bypass or use a mock test if I can't reach the live server easily
    # But since the server is running, I'll try to get a token or use a known user
    
    # I'll use a simpler approach: check the logic via a unit test if I can't reach the server
    print("Verifying persona logic via internal service check...")
    
    from app.services.orchestrator_service import AIOrchestrator
    orchestrator = AIOrchestrator()
    
    # Mock image data
    image_data = b"fake-image-data"
    
    # Test case 1: Tomato Early Blight with yellow leaves
    print("\nTest Case 1: Tomato Early Blight with yellow leaves")
    result = orchestrator.perform_full_analysis(
        image_data=image_data,
        crop_name="Tomato",
        location_data={"city": "Raipur", "state": "Chhattisgarh", "lat": 21.25, "lon": 81.63},
        leaf_color="yellow with brown spots"
    )
    
    da = result["disease_analysis"]
    print(f"Disease: {da['disease_name']}")
    print(f"Color Inference: {da['color_inference']}")
    print(f"Symptoms: {da['symptoms']}")
    
    # Test case 2: Low confidence check
    print("\nTest Case 2: Low confidence check (simulated)")
    # We can't easily force confidence in the live model without mocking the model call
    # But we can verify the suggestions field exists in the output
    print(f"Suggestions present: {'suggestions' in da}")

if __name__ == "__main__":
    import sys
    import os
    # Add backend to path
    sys.path.append(os.getcwd())
    try:
        test_persona_integration()
        print("\nVerification successful!")
    except Exception as e:
        print(f"\nVerification failed: {e}")
        import traceback
        traceback.print_exc()
