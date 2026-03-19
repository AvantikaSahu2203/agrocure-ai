import urllib.parse
from typing import Any, Dict
from .base import BaseAgent
from app.services.ecommerce import generate_search_urls # reusing logic wrapping in agent
# Or implement directly to be self-contained. Let's implement directly for "Clean OOP".

class StoreLinkAgent(BaseAgent):
    """
    Agent responsible for finding products online and nearby.
    Input: Search Term (Medicine Name), Location
    Output: URLs
    """
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data: {
                "query": str, (Medicine name)
                "city": str,
                "state": str
            }
        """
        query = input_data.get("query", "fungicide")
        city = input_data.get("city", "")
        
        encoded_query = urllib.parse.quote(query)
        
        # Amazon & Flipkart
        amazon_url = f"https://www.amazon.in/s?k={encoded_query}"
        flipkart_url = f"https://www.flipkart.com/search?q={encoded_query}"
        
        # Google Maps (Nearby Stores) - Objective 4
        # Specific keywords: "fertilizer shop near me", "krishi seva kendra"
        maps_query = urllib.parse.quote(f"fertilizer shop near {city} krishi seva kendra")
        maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
        
        return {
            "amazon_url": amazon_url,
            "flipkart_url": flipkart_url,
            "maps_url": maps_url,
            "store_hint": f"Search for 'fertilizer shop near me' or 'Krishi Seva Kendra' in {city} for physical availability."
        }
