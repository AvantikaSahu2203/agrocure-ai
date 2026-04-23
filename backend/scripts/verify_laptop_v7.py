import sys
import os
import json

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.orchestrator_service import AIOrchestrator

def run_laptop_demo(image_path, crop="Tomato"):
    print(f"\n{'='*50}")
    print(f" AgroCure AI - Laptop Verification (v7 Ensemble)")
    print(f"{'='*50}\n")
    
    if not os.path.exists(image_path):
        print(f"Error: Image {image_path} not found.")
        return

    with open(image_path, "rb") as f:
        image_data = f.read()

    orchestrator = AIOrchestrator()
    
    # Mock location for Pune
    location = {
        "city": "Pune",
        "state": "Maharashtra",
        "lat": 18.5204,
        "lon": 73.8567,
        "temperature": 32,
        "humidity": 65,
        "rain_forecast": False
    }

    try:
        print(f"Scanning {crop} leaf image: {os.path.basename(image_path)}...")
        result = orchestrator.perform_full_analysis(
            image_data=image_data,
            crop_name=crop,
            location_data=location
        )
        
        # Display nicely
        analysis = result["disease_analysis"]
        medicine = result["medicine_recommendations"]
        
        print("\n[AI ANALYSIS RESULT]")
        print(f"Detected Disease: {analysis['disease_name']}")
        print(f"Confidence:       {analysis['confidence']*100:.1f}%")
        print(f"Severity Level:   {analysis['severity']}")
        print(f"Primary Cause:    {analysis['cause']}")
        
        print("\n[TREATMENT ADVICE]")
        print(f"Chemical: {', '.join(medicine['chemical_treatments'])}")
        print(f"Organic:  {', '.join(medicine['organic_treatments'])}")
        print(f"Dosage:   {medicine['dosage']}")
        
        print("\n[PREVENTION]")
        for tip in medicine['preventative_measures']:
            print(f"• {tip}")

        print(f"\n{'='*50}")
        print(" Verification Complete. Ready for Cloud API deployment.")
        print(f"{'='*50}\n")

    except Exception as e:
        print(f"Verification Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Use absolute path for reliability
    test_img = r"C:\Users\ASUS\Desktop\AgroCure AI\backend\test_image.jpg"
    
    if not os.path.exists(test_img):
        # Fallback to backend root if it's there
        test_img = "test_image.jpg"
        
    run_laptop_demo(test_img, crop="Tomato")
