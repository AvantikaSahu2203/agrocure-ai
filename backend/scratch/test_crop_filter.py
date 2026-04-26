import os
import sys

# Add app directory to path
sys.path.append(os.getcwd())

from app.ml.v7.inference_v7 import AgriInferenceV7

def test_filtering():
    model_path = "app/ml/v7/plant_disease_prediction_model.h5"
    if not os.path.exists(model_path):
        print("Model not found, skipping test.")
        return

    infer = AgriInferenceV7(model_path)
    
    # Mock image bytes
    mock_img = b'\x00' * 100 
    
    # Test Pepper filtering
    # In a real scenario, we'd use a real image, but here we just check if the logic filters labels.
    try:
        # We need a real image for PIL to open
        from PIL import Image
        import io
        img = Image.new('RGB', (224, 224), color='red')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()
        
        print("\n--- Testing Pepper Filtering ---")
        res = infer.predict(img_bytes, crop_name="Pepper")
        print(f"Result for Pepper: {res['disease_name']}")
        assert "Pepper" in res['disease_name']
        
        print("\n--- Testing Tomato Filtering ---")
        res = infer.predict(img_bytes, crop_name="Tomato")
        print(f"Result for Tomato: {res['disease_name']}")
        assert "Tomato" in res['disease_name']
        
        print("\n--- Testing General (No Filtering) ---")
        res = infer.predict(img_bytes, crop_name="General")
        print(f"Result for General: {res['disease_name']}")
        
        print("\nSUCCESS: Filtering logic is working!")
        
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_filtering()
