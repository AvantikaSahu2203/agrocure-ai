import requests
import json
import os
from typing import Dict, List, Optional

class AgriLLMService:
    """
    Service for generating agricultural advice using LLMs and RAG.
    Uses Hugging Face Inference API (free tier).
    """
    HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    
    def __init__(self, hf_token: Optional[str] = None):
        self.hf_token = hf_token or os.getenv("HUGGINGFACE_TOKEN", "")
        self.knowledge_base_path = "app/data/agri_knowledge.json"
        self.knowledge_base = self._load_knowledge_base()

    def _load_knowledge_base(self) -> List[Dict]:
        """Loads the agriculture knowledge base for RAG."""
        if os.path.exists(self.knowledge_base_path):
            with open(self.knowledge_base_path, 'r') as f:
                return json.load(f)
        return []

    def _retrieve_context(self, query: str) -> str:
        """Simple keyword-based retrieval for RAG context."""
        query_words = set(query.lower().split())
        best_match = None
        max_overlap = 0

        for entry in self.knowledge_base:
            overlap = len(query_words.intersection(set(entry["disease"].lower().split())))
            if overlap > max_overlap:
                max_overlap = overlap
                best_match = entry

        if best_match:
            return (f"Disease: {best_match['disease']} ({best_match['scientific_name']})\n"
                    f"Explanation: {best_match['explanation']}\n"
                    f"Causes: {best_match['causes']}\n"
                    f"Chemical Treatment: {best_match['chemical_treatment']}\n"
                    f"Organic Treatment: {best_match['organic_treatment']}\n"
                    f"Prevention: {best_match['preventive_measures']}")
        return "No specific database entry found for this disease."

    def generate_advice(self, crop: str, disease: str) -> Dict:
        """Generates detailed advice using LLM + RAG."""
        query = f"{crop} {disease}"
        context = self._retrieve_context(query)
        
        prompt = f"""
        [INST] You are an expert Agricultural AI Advisor. 
        Provide a detailed report for {crop} affected by {disease}.
        
        Use the following verified knowledge base entry if relevant:
        {context}
        
        Generate the report in JSON format with these keys:
        - explanation: A clear description of the disease.
        - causes: Primary reasons for the infection.
        - chemical_treatment: Recommended pesticides or fungicides.
        - organic_remedies: Natural or home remedies.
        - preventive_measures: Steps to avoid recurrence.
        
        Ensure the advice is professional and safe. If the knowledge base is not specific, use your general knowledge of agriculture.
        [/INST]
        """
        
        headers = {"Authorization": f"Bearer {self.hf_token}"} if self.hf_token else {}
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 1000, "return_full_text": False}
        }

        try:
            if not self.hf_token:
                 # If no token, return high-quality parsed context as fallback
                 return self._parse_context_to_json(context, disease)

            response = requests.post(self.HF_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Basic parsing of LLM response (handling potential non-JSON output)
            text = result[0]['generated_text'] if isinstance(result, list) else result.get('generated_text', "")
            
            # Try to extract JSON from text
            try:
                start = text.find('{')
                end = text.rfind('}') + 1
                if start != -1 and end != -1:
                    return json.loads(text[start:end])
            except:
                pass
                
            return self._parse_context_to_json(context, disease)
            
        except Exception as e:
            print(f"LLM Generation Error: {e}")
            return self._parse_context_to_json(context, disease)

    def _parse_context_to_json(self, context: str, disease: str) -> Dict:
        """Fallback to well-formatted context if LLM fails or no token provided."""
        if "No specific database entry" in context:
            return {
                "explanation": f"The plant shows signs of {disease}. This could be a fungal, bacterial, or viral infection causing tissue damage.",
                "causes": "Common causes include high humidity, poor soil drainage, and pathogen spread via wind or water.",
                "chemical_treatment": "Broad-spectrum fungicide containing Copper or Mancozeb.",
                "organic_remedies": "Neem oil spray (5ml/L) or Garlic-Chili extract.",
                "preventive_measures": "Improve air circulation, avoid overhead watering, and ensure proper crop rotation."
            }
        
        # Simple parsing logic for our own KB format
        lines = context.split('\n')
        data = {}
        for line in lines:
            if ':' in line:
                k, v = line.split(':', 1)
                data[k.strip().lower().replace(' ', '_')] = v.strip()
        
        return {
            "explanation": data.get("explanation", ""),
            "causes": data.get("causes", ""),
            "chemical_treatment": data.get("chemical_treatment", ""),
            "organic_remedies": data.get("organic_treatment", ""),
            "preventive_measures": data.get("prevention", "")
        }

if __name__ == "__main__":
    service = AgriLLMService()
    print(service.generate_advice("Tomato", "Late Blight"))
