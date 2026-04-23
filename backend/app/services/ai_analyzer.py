"""
AI-powered plant disease detection service.
Mock implementation for demonstration - can be replaced with real ML model.
"""
import random
import datetime
import os
import hashlib
from app.services.environmental_risk import EnvironmentalRiskService
from app.services.soil_analysis import SoilAnalysisService
from app.services.llm_service import AgriLLMService
from app.services.medicine_service import MedicineRecommendationService
from typing import Dict, List, Optional

from app.data.disease_data import DISEASE_DATABASE


# Translation Dictionary
TRANSLATION_DATABASE = {
    "hi": {
        "Early Blight": "अगेती झुलसा",
        "Late Blight": "पछेती झुलसा",
        "Leaf Mold": "पत्ती का फफूंद",
        "Rust": "रतुआ",
        "Blast": "झोंका रोग",
        "Potential Fungal Infection": "संभावित फफूंद संक्रमण",
        "Remove affected leaves immediately": "प्रभावित पत्तियों को तुरंत हटा दें",
        "Apply fungicide containing chlorothalonil or mancozeb": "क्लोरोथालोनिल या मैनकोजेब युक्त कवकनाशी का प्रयोग करें",
        "Improve air circulation around plants": "पौधों के आसपास हवा का आवागमन सुधारें",
        "Avoid overhead watering": "ऊपर से पानी देने से बचें",
        "Apply copper-based fungicides immediately": "तुरंत तांबा आधारित कवकनाशी का प्रयोग करें",
        "Remove and destroy infected plants": "संक्रमित पौधों को हटा दें और नष्ट कर दें",
        "Ensure proper spacing for air circulation": "हवा के लिए उचित दूरी सुनिश्चित करें",
        "Monitor weather conditions closely": "मौसम की स्थिति पर कड़ी नजर रखें",
        "Apply protective fungicides": "रक्षात्मक कवकनाशी का प्रयोग करें",
        "Harvest early if disease is severe": "यदि रोग गंभीर है तो जल्दी फसल काट लें",
        "Store only healthy tubers": "केवल स्वस्थ कंदों का भंडारण करें",
        "Apply fungicides at first sign": "पहले संकेत पर कवकनाशी का प्रयोग करें",
        "Use resistant varieties": "रोग प्रतिरोधी किस्मों का प्रयोग करें",
        "Remove volunteer wheat plants": "स्वयं उगने वाले गेहूं के पौधों को हटा दें",
        "Apply tricyclazole or azoxystrobin": "ट्राइसाइक्लाज़ोल या एज़ोक्सीस्ट्रोबिन का प्रयोग करें",
        "Manage nitrogen fertilization": "नाइट्रोजन उर्वरक का प्रबंधन करें",
        "Ensure proper water management": "उचित जल प्रबंधन सुनिश्चित करें",
        "mild": "हल्का",
        "moderate": "मध्यम",
        "severe": "गंभीर",
        "Based on image analysis, the {crop_name} plant shows symptoms consistent with {disease_name} ({scientific_name}).": "छवि विश्लेषण के आधार पर, {crop_name} के पौधे में {disease_name} ({scientific_name}) के लक्षण दिखाई दे रहे हैं।",
        "Current weather conditions ({weather}) may be contributing to disease development.": "वर्तमान मौसम की स्थिति ({weather}) रोग के विकास में योगदान दे सकती है।",
        "The {growth_stage} growth stage makes the plant particularly susceptible to this pathogen.": "{growth_stage} विकास चरण पौधे को इस रोगजनक के प्रति विशेष रूप से संवेदनशील बनाता है।",
        "This disease is commonly observed in the {region} region during this season.": "यह रोग आमतौर पर इस मौसम में {region} क्षेत्र में देखा जाता है।",
        "Immediate action is recommended to prevent further spread.": "तथा प्रसार को रोकने के लिए तत्काल कार्रवाई की सिफारिश की जाती है।",
        "Image analysis suggests potential disease in {crop_name}. For accurate diagnosis, please consult with a local agricultural expert or submit additional images.": "छवि विश्लेषण {crop_name} में संभावित बीमारी का सुझाव देता है। सटीक निदान के लिए, कृपया स्थानीय कृषि विशेषज्ञ से परामर्श करें या अतिरिक्त चित्र जमा करें।",
        "Dark brown spots with concentric rings": "गाढ़े भूरे रंग के धब्बे जिनमें छल्ले हैं",
        "Yellowing around lesions": "घावों के आसपास पीलापन",
        "Leaf curling": "पत्तियों का मुड़ना",
        "Water-soaked lesions": "पानी से लथपथ घाव",
        "White fungal growth on leaf undersides": "पत्तियों के नीचे सफेद फफूंद का विकास",
        "Rapid spreading": "तेजी से फैलना",
        "Pale green or yellow spots on upper leaves": "ऊपरी पत्तियों पर हल्के हरे या पीले धब्बे",
        "Olive-green to brown velvety coating underneath": "नीचे जैतून-हरे से भूरे रंग की मखमली परत",
        "Dark water-soaked lesions": "गहरे पानी से लथपथ घाव",
        "White mold on undersides": "नीचे सफेद फफूंद",
        "Tuber rot": "कंद सड़न",
        "Orange-red pustules on leaves": "पत्तियों पर नारंगी-लाल दाने",
        "Yellow halos around pustules": "दानों के चारों ओर पीला घेरा",
        "Diamond-shaped lesions": "हीरे के आकार के घाव",
        "Gray-white centers with brown margins": "भूरे किनारों के साथ ग्रे-सफेद केंद्र",
        "Discoloration observed": "रंग खराब होना देखा गया",
        "Abnormal leaf patterns detected": "पत्तियों के असामान्य पैटर्न का पता चला",
        "Cucumber": "खीरा",
        "Powdery Mildew": "पाउडरी मिल्ड्यू (सफेद धब्बे)",
        "Downy Mildew": "डाउनी मिल्ड्यू",
        "White powdery spots on leaves": "पत्तियों पर सफेद पाउडर जैसे धब्बे",
        "Stems appearing dusted with flour": "तने आटे से ढके हुए दिखाई देना",
        "Leaf yellowing and drying": "पत्तियों का पीला पड़ना और सूखना",
        "Pepper": "मिर्च",
        "Bacterial Spot": "जीवाणु धब्बा (Bacterial Spot)",
        "Early Blight": "अगेती झुलसा",
        "Fungal Spot": "कवक धब्बा (Fungal Spot)",
        "Leaf Spot": "पत्ता धब्बा",
        "Mite Damage": "माइट का प्रकोप",
        "Viral Mosaic": "मोजेक वायरस",
        "Fusarium Wilt": "फ्यूसेरियम विल्ट (मुरझाना)",
        "Anthracnose": "एंथ्रेकनोज (Anthracnose)",
        "Mosaic Virus": "मोजेक वायरस",
        "Healthy": "स्वस्थ"
    },
    "mr": {
        "Early Blight": "करपा",
        "Late Blight": "उशिरा येणारा करपा",
        "Leaf Mold": "पानांवरील बुरशी",
        "Rust": "तांबेरा",
        "Blast": "करपा (भात)",
        "Potential Fungal Infection": "संभावित बुरशीजन्य संसर्ग",
        "Remove affected leaves immediately": "प्रभावित पाने त्वरित काढून टाका",
        "Apply fungicide containing chlorothalonil or mancozeb": "क्लोरोथॅलोनिल किंवा मॅन्कोझेबयुक्त बुरशीनाशकाची फवारणी करा",
        "Improve air circulation around plants": "रोपांभोवती हवा खेळती राहील याची काळजी घ्या",
        "Avoid overhead watering": "वरून पाणी देणे टाळा",
        "Apply copper-based fungicides immediately": "त्वरित कॉपर-आधारित बुरशीनाशकांचा वापर करा",
        "Remove and destroy infected plants": "संसर्ग झालेली झाडे काढून टाका आणि नष्ट करा",
        "Ensure proper spacing for air circulation": "हवा खेळती राहण्यासाठी योग्य अंतर ठेवा",
        "Monitor weather conditions closely": "हवामानाच्या स्थितीवर बारकाईने लक्ष ठेवा",
        "Apply protective fungicides": "संरक्षणात्मक बुरशीनाशकांचा वापर करा",
        "Harvest early if disease is severe": "रोग गंभीर असल्यास लवकर काढणी करा",
        "Store only healthy tubers": "केवळ निरोगी कंदांची साठवणूक करा",
        "Apply fungicides at first sign": "पहिली लक्षणे दिसताच बुरशीनाशकाचा वापर करा",
        "Use resistant varieties": "रोगप्रतिकारक जातींचा वापर करा",
        "Remove volunteer wheat plants": "आपोआप उगवलेली गव्हाची झाडे काढून टाका",
        "Apply tricyclazole or azoxystrobin": "ट्रायसायक्लाझोल किंवा अॅझोक्सिस्ट्रोबिनचा वापर करा",
        "Manage nitrogen fertilization": "नायट्रोजन खताचे व्यवस्थापन करा",
        "Ensure proper water management": "पाण्याचे योग्य व्यवस्थापन करा",
        "mild": "सौम्य",
        "moderate": "मध्यम",
        "severe": "गंभीर",
        "Based on image analysis, the {crop_name} plant shows symptoms consistent with {disease_name} ({scientific_name}).": "प्रतिमा विश्लेषणावरून असे दिसून येते की {crop_name} रोपावर {disease_name} ({scientific_name}) ची लक्षणे आहेत.",
        "Current weather conditions ({weather}) may be contributing to disease development.": "सध्याची हवामान स्थिती ({weather}) रोगाच्या वाढीस कारणीभूत ठरू शकते.",
        "The {growth_stage} growth stage makes the plant particularly susceptible to this pathogen.": "{growth_stage} वाढीच्या टप्प्यामुळे रोप या रोगास लवकर बळी पडू शकते.",
        "This disease is commonly observed in the {region} region during this season.": "हा रोग साधारणपणे या हंगामात {region} विभागात आढळून येतो.",
        "Immediate action is recommended to prevent further spread.": "पुढील प्रसार रोखण्यासाठी त्वरित कारवाई करण्याची शिफारस केली जाते.",
        "Image analysis suggests potential disease in {crop_name}. For accurate diagnosis, please consult with a local agricultural expert or submit additional images.": "प्रतिमा विश्लेषण {crop_name} मध्ये संभाव्य रोगाचे संकेत देते. अचूक निदानासाठी, कृपया स्थानिक कृषी तज्ञाचा सल्ला घ्या किंवा अतिरिक्त प्रतिमा जमा करा.",
        "Dark brown spots with concentric rings": "गडद तपकिरी ठिपके ज्यात वलये आहेत",
        "Yellowing around lesions": "जखमांच्या भोवती पिवळसरपणा",
        "Leaf curling": "पाने वाकडी होणे",
        "Water-soaked lesions": "पाण्याने भरलेले डाग",
        "White fungal growth on leaf undersides": "पानांच्या खालील बाजूस पांढरी बुरशी",
        "Rapid spreading": "वेगाने पसरणे",
        "Pale green or yellow spots on upper leaves": "वरच्या पानांवर फिकट हिरवे किंवा पिवळे ठिपके",
        "Olive-green to brown velvety coating underneath": "खालील बाजूस ऑलिव्ह-हिरव्या ते तपकिरी रंगाचा मखमली लेप",
        "Dark water-soaked lesions": "गडद पाण्याने भरलेले डाग",
        "White mold on undersides": "खालील बाजूस पांढरी बुरशी",
        "Tuber rot": "कंद कुजणे",
        "Orange-red pustules on leaves": "पानांवर नारंगी-लाल फोड",
        "Yellow halos around pustules": "फोडांच्या भोवती पिवळे वलय",
        "Diamond-shaped lesions": "हियराच्या आकाराचे डाग",
        "Gray-white centers with brown margins": "तपकिरी कडा असलेले राखाडी-पांढरे केंद्र",
        "Discoloration observed": "रंग बदललेला आढळला",
        "Abnormal leaf patterns detected": "पानांवर असामान्य नक्षी आढळली",
        "Cucumber": "काकडी",
        "Powdery Mildew": "भुरी रोग (पांढरे ठिपके)",
        "Downy Mildew": "केवडा रोग",
        "White powdery spots on leaves": "पानांवर पांढरे पिठासारखे ठिपके",
        "Stems appearing dusted with flour": "देठ पिठाने माखल्यासारखे दिसणे",
        "Leaf yellowing and drying": "पाने पिवळी पडणे आणि सुकणे",
        "Pepper": "मिरची",
        "Bacterial Spot": "जिवाणूजन्य ठिपके (Bacterial Spot)",
        "Early Blight": "करपा (Early Blight)",
        "Fungal Spot": "बुरशीजन्य ठिपके",
        "Leaf Spot": "पानांवरील ठिपके",
        "Mite Damage": "कोळी कीड नुकसान",
        "Viral Mosaic": "मोझॅक व्हायरस",
        "Healthy": "निरोगी"
    }
}


class AIPlantAnalyzer:
    """Enhanced AI analyzer for plant disease detection.
    Uses AgriInferenceV5 for ML results with deterministic mock fallback.
    """
    def __init__(self):
        self.v7_engine = None
        self._load_model()
        self.env_risk_service = EnvironmentalRiskService()
        self.soil_analysis_service = SoilAnalysisService()
        self.llm_service = AgriLLMService()
        self.medicine_service = MedicineRecommendationService()
        
    def _load_model(self):
        """Attempts to load the ML engine if the model file is present."""
        if self.v7_engine:
            return True
            
        try:
            from app.ml.v7.inference_v7 import AgriInferenceV7
            # Path for V7 Keras model
            model_path = os.path.join("app", "ml", "v7", "plant_disease_prediction_model.h5")
            if os.path.exists(model_path):
                self.v7_engine = AgriInferenceV7(
                    model_path=model_path,
                    device="cpu"
                )
                print(f"V7 Keras Engine loaded successfully.")
                return True
        except Exception as e:
            print(f"V7 ML Engine loading failed: {e}")
        return False
        
        self.env_risk_service = EnvironmentalRiskService()
        self.soil_analysis_service = SoilAnalysisService()
        self.llm_service = AgriLLMService()
        self.medicine_service = MedicineRecommendationService()

    def analyze_image(
        self,
        crop_name: str,
        image_data: bytes,
        region: Optional[str] = None,
        weather: Optional[str] = None,
        growth_stage: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        soil_ph: Optional[float] = None,
        soil_n: Optional[float] = None,
        soil_p: Optional[float] = None,
        soil_k: Optional[float] = None,
        language: str = "en"
    ) -> Dict:
        """
        Analyze crop image for disease detection.
        Uses AgriInferenceV4 if available, otherwise falls back to deterministic mock.
        """
        import tempfile
        import cv2
        import numpy as np
        
        # 0. Pre-process image for all steps
        nparr = np.frombuffer(image_data, np.uint8)
        img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # 1. Image-based Analysis (High-Precision Modular Orchestrator)
        v7_result = None
        if image_data:
            try:
                # Use the specialized DiseaseDetectionAgent for multi-model switching
                from app.agents.disease_agent import DiseaseDetectionAgent
                diag_agent = DiseaseDetectionAgent()
                
                # Execute diagnosis with crop context
                diag_result = diag_agent.execute({
                    "image": image_data,
                    "crop_name": crop_name,
                    "weather_context": weather,
                    "growth_stage": growth_stage
                })
                
                # Map agent result back to v7_result format for backward compatibility
                v7_result = {
                    "disease_name": diag_result["disease_name"],
                    "confidence": diag_result["confidence"],
                    "severity": 0.8 if diag_result["severity"] == "High" else 0.4,
                    "status": "Success" if diag_result["confidence"] > 0.4 else "Uncertain"
                }
                print(f"DEBUG: Specialized Analysis Success. Result: {v7_result['disease_name']} ({v7_result['confidence']})")
            except Exception as e:
                print(f"Specialized Inference Error: {e}")

        # 1b. Fallback "White Spot" detection if model is not trained/present
        white_spot_detected = False
        if (not self.v7_engine or (v7_result and v7_result.get("status") == "Uncertain")) and img_bgr is not None:
            try:
                # Simple rule-based "White Spot" detection for Powdery Mildew
                gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
                # Threshold for high-luminance (white-ish) spots
                _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
                white_pixels = cv2.countNonZero(thresh)
                total_pixels = gray.shape[0] * gray.shape[1]
                white_ratio = white_pixels / total_pixels
                
                print(f"DEBUG: White Spot Detection - Ratio: {white_ratio:.4f}")
                
                # If significant white area found, assume Powdery Mildew for Cucumber
                if white_ratio > 0.02: # 2% of image is bright white
                    white_spot_detected = True
            except Exception as e:
                print(f"Fallback Detection Error: {e}")

        # 2. Environmental Risk Analysis
        env_risk = None
        if lat is not None and lon is not None:
            try:
                env_risk = self.env_risk_service.predict_risk(lat, lon)
            except Exception as e:
                print(f"Environmental Risk Error: {e}")

        # 3. Soil Analysis
        soil_result = None
        if all(v is not None for v in [soil_ph, soil_n, soil_p, soil_k]):
            try:
                soil_result = self.soil_analysis_service.analyze_soil(soil_ph, soil_n, soil_p, soil_k)
            except Exception as e:
                print(f"Soil Analysis Error: {e}")

        crop_lower = crop_name.lower()
        
        # Get diseases for this crop
        crop_diseases = DISEASE_DATABASE.get(crop_lower, [])
        
        # DETERMINISTIC MOCK / FALLBACK: Select a disease based on image hash
        img_hash = hashlib.md5(image_data).hexdigest()
        hash_int = int(img_hash, 16)
        
        if v7_result:
            # Handle Uncertainty logic from requirements
            if v7_result.get("status") == "Uncertain":
                # Requirement: If symptoms detected but classification uncertain, 
                # classify as "Potential Disease – Further Analysis Required"
                return {
                    "disease_name": "Potential Disease – Further Analysis Required",
                    "scientific_name": "N/A",
                    "confidence": v7_result["confidence"],
                    "severity": "Unknown",
                    "symptoms_detected": ["Awaiting clearer image for spot analysis"],
                    "analysis": v7_result.get("message", "Classification uncertain."),
                    "recommendations": [
                        "Please capture a clearer, high-resolution image",
                        "Ensure lesions are in focus",
                        "Avoid direct glare or dark shadows"
                    ],
                    "affected_area_percentage": 0,
                    "crop_info": {
                        "name": crop_name,
                        "growth_stage": growth_stage or "Unknown",
                        "region": region or "Unknown"
                    },
                    "timestamp": datetime.datetime.utcnow().isoformat()
                }

            # Match v5 result to local database
            mapped_disease_name = v7_result["disease_name"]
            
            # Find matching disease in DB by name
            selected_disease = next((d for d in crop_diseases if d["name"].lower() == mapped_disease_name.lower()), None)
            
            if not selected_disease:
                # Fallback to generic if name doesn't exist in DB
                selected_disease = {
                    "name": mapped_disease_name,
                    "scientific_name": "Detected via AgriNet-V7",
                    "symptoms": ["Anomalies detected in imagery"],
                    "recommendations": ["Consult local guidelines for " + mapped_disease_name]
                }

            confidence = v7_result["confidence"]
            severity_val = v7_result["severity"] * 100
        else:
            if not crop_diseases:
                response = self._generic_disease_response(crop_name)
                if language != "en":
                    return self._translate_response(response, language, crop_name)
                return response
            
            disease_index = hash_int % len(crop_diseases)
            selected_disease = crop_diseases[disease_index]
            conf_seed = int(img_hash[:4], 16) / 65535.0
            base_confidence = 0.85 + (conf_seed * 0.13)
            
            # Adjust confidence based on context (still deterministic if context is same)
            if weather and "humid" in weather.lower():
                base_confidence += 0.02
                
            # If fallback detected white spots, force Powdery Mildew for Cucumber
            if white_spot_detected and crop_lower == "cucumber":
                pm_disease = next((d for d in crop_diseases if d["name"] == "Powdery Mildew"), None)
                if pm_disease:
                    selected_disease = pm_disease
                    base_confidence = 0.92
            
            confidence = min(base_confidence, 0.99)
            severity_val = None # Use mock severity calc

        # Determine severity string
        if severity_val is not None:
            if severity_val > 50: severity = "severe"
            elif severity_val > 20: severity = "moderate"
            else: severity = "mild"
        else:
            severity = self._calculate_severity(confidence, image_data)
        
        # Calculate affected area percentage
        affected_area = self._estimate_affected_area(severity, img_hash)
        if severity_val is not None:
            affected_area = int(severity_val) # Use ML severity as area for consistency
        
        # Get medicines from specialized database
        meds = self.medicine_service.get_recommendation(selected_disease["name"])
        
        # Expert Fix: If Healthy, ensure recommendations are preventive/prophylactic
        recommendations = selected_disease["recommendations"]
        chemical_treatment = meds["chemical_medicine"]
        organic_treatment = meds["organic_remedy"]
        dosage = selected_disease.get("dosage", "As per package instructions")

        if selected_disease["name"].lower() == "healthy":
            chemical_treatment = "None required"
            organic_treatment = "General plant care and nutrition"
            dosage = "N/A"
            recommendations = [
                "Continue regular monitoring",
                "Ensure balanced fertilization",
                "Maintain optimal irrigation",
                "Implement preventive neem oil spray if neighboring plants are infected"
            ]

        result = {
            "disease_name": selected_disease["name"],
            "scientific_name": selected_disease["scientific_name"],
            "confidence": float(f"{confidence:.2f}"),
            "severity": severity,
            "symptoms_detected": selected_disease["symptoms"],
            "chemical_treatment": chemical_treatment,
            "organic_treatment": organic_treatment,
            "dosage": dosage,
            "analysis": self._generate_analysis(
                selected_disease, crop_name, region, weather, growth_stage
            ),
            "recommendations": recommendations,
            "affected_area_percentage": affected_area,
            "crop_info": {
                "name": crop_name,
                "growth_stage": growth_stage or "Unknown",
                "region": region or "Unknown",
                "ml_detected_crop": v7_result.get("disease_name") if v7_result else "Mocked"
            },
            "environmental_risk": env_risk,
            "soil_analysis": soil_result,
            "llm_reasoning": self.llm_service.generate_advice(crop_name, selected_disease["name"]),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        
        if language != "en":
            return self._translate_response(result, language, crop_name)
            
        return result
    
    def _translate_response(self, response: Dict, language: str, crop_name: str) -> Dict:
        """Translate response dictionary to target language with template reconstruction."""
        translations = TRANSLATION_DATABASE.get(language, {})
        if not translations:
            return response
            
        translated = response.copy()
        
        # Translate simple fields
        translated["disease_name"] = translations.get(response["disease_name"], response["disease_name"])
        translated["severity"] = translations.get(response["severity"], response["severity"])
        
        # Translate lists
        translated["symptoms_detected"] = [translations.get(s, s) for s in response["symptoms_detected"]]
        translated["recommendations"] = [translations.get(r, r) for r in response["recommendations"]]
        
        # Reconstruct analysis using translated templates
        template_key_base = "Based on image analysis, the {crop_name} plant shows symptoms consistent with {disease_name} ({scientific_name})."
        translated_template_base = translations.get(template_key_base, template_key_base)
        
        # Build analysis parts
        analysis_parts = [
            translated_template_base.format(
                crop_name=crop_name,
                disease_name=translated["disease_name"],
                scientific_name=response["scientific_name"]
            )
        ]
        
        if response["crop_info"]["region"] != "Unknown":
            reg_key = "This disease is commonly observed in the {region} region during this season."
            translated_reg = translations.get(reg_key, reg_key)
            analysis_parts.append(translated_reg.format(region=response["crop_info"]["region"]))
            
        imm_key = "Immediate action is recommended to prevent further spread."
        analysis_parts.append(translations.get(imm_key, imm_key))
        
        translated["analysis"] = " ".join(analysis_parts)
        
        return translated

    def _calculate_severity(self, confidence: float, image_data: bytes) -> str:
        """Calculate disease severity level."""
        # Mock severity calculation based on confidence
        if confidence > 0.94:
            return "severe"
        elif confidence > 0.88:
            return "moderate"
        else:
            return "mild"
    
    def _estimate_affected_area(self, severity: str, img_hash: Optional[str] = None) -> int:
        """Estimate percentage of affected area deterministically if hash provided."""
        severity_ranges = {
            "mild": (5, 20),
            "moderate": (20, 50),
            "severe": (50, 85)
        }
        
        range_min, range_max = severity_ranges.get(severity, (10, 30))
        
        if img_hash:
            # Use hash for deterministic area
            hash_val = int(img_hash[-2:], 16) # use last 2 chars
            area = range_min + (hash_val % (range_max - range_min + 1))
            return area
            
        return random.randint(range_min, range_max)
    
    def _generate_analysis(
        self,
        disease: Dict,
        crop_name: str,
        region: Optional[str],
        weather: Optional[str],
        growth_stage: Optional[str]
    ) -> str:
        """Generate detailed analysis text."""
        analysis_parts = [
            f"Based on image analysis, the {crop_name} plant shows symptoms consistent with {disease['name']} ({disease['scientific_name']})."
        ]
        
        if weather:
            analysis_parts.append(f"Current weather conditions ({weather}) may be contributing to disease development.")
        
        if growth_stage:
            analysis_parts.append(f"The {growth_stage} growth stage makes the plant particularly susceptible to this pathogen.")
        
        if region:
            analysis_parts.append(f"This disease is commonly observed in the {region} region during this season.")
        
        analysis_parts.append("Immediate action is recommended to prevent further spread.")
        
        return " ".join(analysis_parts)
    
    def _generic_disease_response(self, crop_name: str) -> Dict:
        """Return generic response for unknown crops."""
        return {
            "disease_name": "Potential Fungal Infection",
            "scientific_name": "Unknown pathogen",
            "confidence": 0.65,
            "severity": "moderate",
            "symptoms_detected": [
                "Discoloration observed",
                "Abnormal leaf patterns detected"
            ],
            "analysis": f"Image analysis suggests potential disease in {crop_name}. For accurate diagnosis, please consult with a local agricultural expert or submit additional images.",
            "recommendations": [
                "Isolate affected plants",
                "Monitor for symptom progression",
                "Consult local agricultural extension service",
                "Consider laboratory testing for precise identification"
            ],
            "affected_area_percentage": 25,
            "crop_info": {
                "name": crop_name,
                "growth_stage": "Unknown",
                "region": "Unknown"
            },
            "timestamp": datetime.datetime.utcnow().isoformat()
        }


# Singleton instance
ai_analyzer = AIPlantAnalyzer()
