import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.curdir))

from app.services.llm_service import AgriLLMService

def test_llm_advice():
    print("--- AgriLLM Advisory Verification ---")
    
    # Initialize service
    service = AgriLLMService()
    
    # Test case: Tomato Late Blight (should hit RAG)
    print("\nTesting: Tomato + Late Blight (RAG Hit)")
    advice = service.generate_advice("Tomato", "Late Blight")
    
    print("\nLLM/RAG Output:")
    print(f"Explanation: {advice.get('explanation')[:100]}...")
    print(f"Causes: {advice.get('causes')[:100]}...")
    print(f"Chemical: {advice.get('chemical_treatment')}")
    print(f"Organic: {advice.get('organic_remedies')}")
    
    # Test case: Generic (should hit LLM Fallback)
    print("\nTesting: Corn + Rust (Heuristic Fallback)")
    advice_fallback = service.generate_advice("Corn", "Rust")
    print(f"Explanation: {advice_fallback.get('explanation')}")

    if "late blight" in advice.get('explanation', "").lower() or "oomycete" in advice.get('causes', "").lower():
        print("\nVerification: SUCCESS")
    else:
        print("\nVerification: CHECK OUTPUTS")

if __name__ == "__main__":
    test_llm_advice()
