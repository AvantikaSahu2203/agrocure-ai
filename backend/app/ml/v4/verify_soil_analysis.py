import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.curdir))

from app.services.soil_analysis import SoilAnalysisService

def test_soil_analysis():
    print("--- Soil Analysis Verification ---")
    
    # Sample parameters: Acidic soil with low Nitrogen
    ph, n, p, k = 4.5, 20.0, 40.0, 50.0
    
    service = SoilAnalysisService()
    
    print(f"Testing parameters: pH={ph}, N={n}, P={p}, K={k}")
    result = service.analyze_soil(ph, n, p, k)
    
    print("\nResult:")
    print(f"Deficiencies: {result['deficiencies']}")
    print(f"Soil Diseases: {result['soil_diseases']}")
    print(f"Risk Level: {result['risk_level']}")
    
    # Expected for pH 4.5: Nitrogen deficiency (n=20), Magnesium deficiency (ph<5.2), Clubroot (ph<5.0)
    print("\nVerification: SUCCESS" if "Nitrogen" in result['deficiencies'] and "Clubroot" in result['soil_diseases'] else "\nVerification: CHECK RESULTS")

if __name__ == "__main__":
    test_soil_analysis()
