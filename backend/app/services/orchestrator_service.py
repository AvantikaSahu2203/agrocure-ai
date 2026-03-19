from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from app.agents.disease_agent import DiseaseDetectionAgent
from app.agents.medicine_agent import MedicineRecommendationAgent
from app.agents.weather_agent import WeatherRiskAgent
from app.agents.store_agent import StoreLinkAgent

class AIOrchestrator:
    """
    Coordinating brain that manages the lifecycle of a crop analysis request.
    """
    
    def __init__(self):
        self.disease_agent = DiseaseDetectionAgent()
        self.medicine_agent = MedicineRecommendationAgent()
        self.weather_agent = WeatherRiskAgent()
        self.store_agent = StoreLinkAgent()
        
    def perform_full_analysis(self, 
                            image_data: bytes, 
                            crop_name: str, 
                            location_data: Dict[str, Any],
                            weather_context: Optional[str] = None,
                            leaf_color: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes the analysis pipeline:
        Image -> Disease -> Medicine -> Links -> Weather -> Final Report
        """
        
        # 1. Detect Disease
        disease_input = {
            "image": image_data,
            "crop_name": crop_name,
            "weather_context": weather_context,
            "leaf_color": leaf_color
        }
        disease_result = self.disease_agent.execute(disease_input)
        
        # 2. Recommend Medicine
        medicine_input = {
            "disease_name": disease_result["disease_name"],
            "crop_name": crop_name
        }
        medicine_result = self.medicine_agent.execute(medicine_input)
        
        # 3. Generate Store Links
        # search for the chemical treatment found
        chemical_meds = medicine_result.get("chemical_treatments", [])
        search_query = chemical_meds[0] if chemical_meds else "agricultural fungicide"
            
        store_input = {
            "query": search_query,
            "city": location_data.get("city"),
            "state": location_data.get("state")
        }
        store_result = self.store_agent.execute(store_input)
        
        # 4. Assess Weather Risk
        weather_input = {
            "lat": location_data.get("lat"),
            "lon": location_data.get("lon"),
            "humidity": location_data.get("humidity"),
            "temperature": location_data.get("temperature"),
            "rain_forecast": location_data.get("rain_forecast")
        }
        weather_result = self.weather_agent.execute(weather_input)
        
        # 5. Combine Results
        final_report = {
            "disease_analysis": disease_result,
            "medicine_recommendations": medicine_result,
            "ecommerce_links": store_result,
            "weather_risk": weather_result,
            "timestamp": disease_result["detected_at"]
        }
        
        return final_report
