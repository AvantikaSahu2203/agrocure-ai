import sys
import os

# Add the project root to sys.path
sys.path.append(r"C:\Users\ASUS\Desktop\AgroCure AI\backend")

from app.agents.disease_agent import DiseaseDetectionAgent

def test_watermelon_routing():
    print("--- Starting Watermelon Routing Test ---")
    agent = DiseaseDetectionAgent()
    
    # Simulate a small blank image (since we aren't loading real pixels)
    mock_image = b'\x00' * 1024
    
    input_data = {
        "image": mock_image,
        "crop_name": "watermelon",
        "leaf_color": "green"
    }
    
    print("\n[Test] Executing agent with crop_name='watermelon'...")
    try:
        result = agent.execute(input_data)
        
        print("\n--- Test Result ---")
        print(f"Disease Name: {result.get('disease_name')}")
        print(f"Scientific Name: {result.get('scientific_name')}")
        print(f"Confidence: {result.get('confidence')}")
        print(f"Is Specialized: {result.get('is_specialized', False)}")
        
        # Verify it uses the Watermelon class list
        # "Healthy" is a class in our watermelon engine
        if result.get('is_specialized') and "Citrullus" in result.get('scientific_name', ''):
            print("\nSUCCESS: Request correctly routed to Specialized Watermelon Engine!")
        else:
            print("\nFAILURE: Request was NOT correctly routed to Watermelon Engine.")
            
    except Exception as e:
        print(f"\nERROR during execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_watermelon_routing()
