# Centralized Disease and Treatment Database for AgroCure AI
# Contains high-quality, ICAR-standard chemical and organic recommendations.

DISEASE_DATABASE = {
    "tomato": [
        {
            "name": "Early Blight",
            "scientific_name": "Alternaria solani",
            "cause": "Fungal infection due to high humidity and warm weather",
            "symptoms": ["Yellow leaves with brown circular spots", "Leaves drying from the bottom", "Target-like rings on spots"],
            "severity_indicators": ["spot_size", "leaf_coverage", "yellowing"],
            "chemical_treatment": "Amistar (Azoxystrobin) or Kavach (Chlorothalonil)",
            "organic_treatment": "Neem oil or Baking soda solution (5g/L)",
            "dosage": "2ml per liter of water, spray every 10 days",
            "recommendations": [
                "Remove affected leaves immediately",
                "Apply fungicide containing chlorothalonil or azoxystrobin",
                "Improve air circulation around plants",
                "Avoid overhead watering"
            ]
        },
        {
            "name": "Late Blight",
            "scientific_name": "Phytophthora infestans",
            "cause": "Fungal infection spreading rapidly in cool, wet weather",
            "symptoms": ["Dark water-soaked patches on leaves", "White fuzzy growth on leaf undersides", "Plants wilting quickly"],
            "severity_indicators": ["lesion_size", "spread_rate", "fungal_growth"],
            "chemical_treatment": "Ridomil Gold (Metalaxyl + Mancozeb)",
            "organic_treatment": "Copper-based fungicides (Bordeaux mixture)",
            "dosage": "2.5g per liter, spray immediately upon detection",
            "recommendations": [
                "Apply copper-based fungicides immediately",
                "Remove and destroy infected plants",
                "Ensure proper spacing for air circulation",
                "Monitor weather conditions closely"
            ]
        },
        {
            "name": "Leaf Mold",
            "scientific_name": "Passalora fulva",
            "cause": "Fungal disease caused by high humidity and poor ventilation",
            "symptoms": ["Hazy yellow spots on upper leaves", "Velvety olive-green mold on the bottom of leaves", "Leaves curling and dropping"],
            "severity_indicators": ["spot_density", "coating_coverage"],
            "chemical_treatment": "Score (Difenoconazole)",
            "organic_treatment": "Sulfur dust or biological controls (Bacillus subtilis)",
            "dosage": "1ml per liter, apply every 14 days",
            "recommendations": [
                "Reduce humidity in growing area",
                "Improve ventilation",
                "Apply fungicides if severe",
                "Remove heavily infected leaves"
            ]
        },
        {
            "name": "Bacterial Spot",
            "scientific_name": "Xanthomonas perforans",
            "symptoms": ["Small, water-soaked spots", "Spots turning black with yellow halo"],
            "severity_indicators": ["spot_count", "blackening"],
            "chemical_treatment": "Copper/Mancozeb mix",
            "organic_treatment": "Neem spray",
            "dosage": "2g per liter",
            "recommendations": ["Avoid touching plants when wet", "Use drip irrigation"]
        },
        {
            "name": "Healthy",
            "scientific_name": "Solanum lycopersicum (Healthy)",
            "symptoms": ["Dark green leaves", "Robust stems"],
            "recommendations": ["Monitor for pests", "Prune suckers"]
        }
    ],
    "potato": [
        {
            "name": "Late Blight",
            "scientific_name": "Phytophthora infestans",
            "symptoms": ["Dark water-soaked lesions", "White mold on undersides", "Tuber rot"],
            "severity_indicators": ["lesion_coverage", "tuber_damage"],
            "chemical_treatment": "Ridomil Gold or Indofil M-45 (Mancozeb)",
            "organic_treatment": "Copper oxychloride",
            "dosage": "3g per liter, preventive spray recommended",
            "recommendations": [
                "Apply protective fungicides",
                "Destroy infected plants",
                "Harvest early if disease is severe",
                "Store only healthy tubers"
            ]
        },
        {
            "name": "Early Blight",
            "scientific_name": "Alternaria solani",
            "symptoms": ["Target-like spots with concentric rings", "Leaf yellowing"],
            "severity_indicators": ["spot_count", "leaf_yellowing"],
            "chemical_treatment": "Chlorothalonil or Azoxystrobin",
            "organic_treatment": "Neem oil",
            "dosage": "2ml per liter",
            "recommendations": [
                "Rotate with non-solanaceous crops",
                "Maintain plant vigor with balanced nutrition"
            ]
        },
        {
            "name": "Healthy",
            "scientific_name": "Solanum tuberosum (Healthy)",
            "symptoms": ["Lush green foliage", "No lesions"],
            "recommendations": ["Normal irrigation", "Hill up tubers"]
        }
    ],
    "wheat": [
        {
            "name": "Rust",
            "scientific_name": "Puccinia spp.",
            "cause": "Fungal spores spread by wind",
            "symptoms": ["Orange-red powdery spots on leaves", "Yellow circles around the spots", "Leaves turning dry"],
            "severity_indicators": ["pustule_density", "leaf_coverage"],
            "chemical_treatment": "Tilt (Propiconazole) or Follicur (Tebuconazole)",
            "organic_treatment": "Remove infected plants, avoid nitrogen excess",
            "dosage": "1ml per liter at flag leaf stage",
            "recommendations": [
                "Apply fungicides at first sign",
                "Use resistant varieties",
                "Remove volunteer wheat plants",
                "Monitor weather conditions"
            ]
        }
    ],
    "rice": [
        {
            "name": "Blast",
            "scientific_name": "Magnaporthe oryzae",
            "cause": "Fungal infection triggered by high nitrogen and humid nights",
            "symptoms": ["Boat-shaped or diamond-shaped spots on leaves", "Gray centers with brown borders", "Neck of the plant turning black and breaking"],
            "severity_indicators": ["lesion_count", "panicle_infection"],
            "chemical_treatment": "Baan (Tricyclazole) or Hinosan (Edifenphos)",
            "organic_treatment": "Pseudomonas fluorescens (Bio-control)",
            "dosage": "0.6g per liter, spray at tillering stage",
            "recommendations": [
                "Apply tricyclazole or azoxystrobin",
                "Manage nitrogen fertilization",
                "Ensure proper water management",
                "Use resistant varieties"
            ]
        },
        {
            "name": "Bacterial Blight",
            "scientific_name": "Xanthomonas oryzae",
            "symptoms": ["Yellowing of leaf tips", "Wavy margins on lesions", "Bacterial ooze"],
            "chemical_treatment": "Streptomycin + Tetracycline (Streptocycline)",
            "organic_treatment": "Bleaching powder drenching @ 10kg/ha",
            "recommendations": ["Drain field", "Avoid excess Nitrogen"]
        },
        {
            "name": "Brown Spot",
            "scientific_name": "Cochliobolus miyabeanus",
            "symptoms": ["Oval brown spots with gray centers"],
            "chemical_treatment": "Mancozeb or Propiconazole",
            "organic_treatment": "Seed treatment with Trichoderma viride",
            "recommendations": ["Apply balanced nutrients (N-P-K)"]
        }
    ],
    "cotton": [
        {
            "name": "Boll Rot",
            "scientific_name": "Colletotrichum capsici",
            "symptoms": ["Brown water-soaked spots on bolls", "Bolls fail to open", "Internal lint decay"],
            "chemical_treatment": "Blitox (Copper Oxychloride)",
            "organic_treatment": "Seed treatment with Trichoderma viride",
            "dosage": "2.5g per liter, spray during boll development",
            "recommendations": [
                "Avoid excessive nitrogen",
                "Ensure proper plant spacing",
                "Remove and burn infected bolls"
            ]
        }
    ],
    "mango": [
        {
            "name": "Anthracnose",
            "scientific_name": "Colletotrichum gloeosporioides",
            "symptoms": ["Black slightly sunken spots on fruits", "Leaft tip dieback", "Blossom blight"],
            "chemical_treatment": "Contaf (Hexaconazole) or Bavistin (Carbendazim)",
            "organic_treatment": "Spray Dashparni Ark or Neem oil",
            "dosage": "2ml per liter, apply twice before flowering",
            "recommendations": [
                "Prune dead twigs and burn them",
                "Maintain orchard sanitation",
                "Avoid injury to fruits during harvest"
            ]
        }
    ],
    "cucumber": [
        {
            "name": "Powdery Mildew",
            "scientific_name": "Podosphaera xanthii",
            "cause": "Fungal infection favored by warm, dry days and cool, humid nights",
            "symptoms": ["White flour-like powder on leaves and stems", "Leaves turning yellow and then brown", "Stunted fruit growth"],
            "severity_indicators": ["spot_density", "leaf_coverage"],
            "chemical_treatment": "Karathane (Dinocap) or Bayleton (Triadimefon)",
            "organic_treatment": "Milk spray (1:9 ratio) or Neem oil",
            "dosage": "5ml per liter, spray every 7 days",
            "recommendations": [
                "Increase air circulation",
                "Reduce shade",
                "Apply sulfur-based fungicides",
                "Remove and burn heavily infected leaves"
            ]
        },
        {
            "name": "Downy Mildew",
            "scientific_name": "Pseudoperonospora cubensis",
            "symptoms": ["Angular yellow spots on upper leaf surface", "Purplish-gray fungus on leaf undersides"],
            "severity_indicators": ["angular_spot_count", "underside_growth"],
            "chemical_treatment": "Ridomil Gold or Curzate",
            "organic_treatment": "Copper fungicides",
            "dosage": "2g per liter, apply upon first sign",
            "recommendations": [
                "Avoid overhead irrigation",
                "Improve plant spacing",
                "Monitor humidity levels"
            ]
        }
    ],
    "pepper": [
        {
            "name": "Bacterial Spot",
            "scientific_name": "Xanthomonas campestris pv. vesicatoria",
            "symptoms": ["Small yellow-green lesions", "Angular spots on leaves", "Pustules on leaf undersides"],
            "severity_indicators": ["spot_density", "lesion_size"],
            "chemical_treatment": "Copper-based fungicides or Streptomycin",
            "organic_treatment": "Neem oil or Serenade (Bacillus subtilis)",
            "dosage": "2.5g per liter, spray every 10-14 days",
            "recommendations": [
                "Using pathogen-free seeds",
                "Remove and burn infected plant debris",
                "Rotate with non-host crops like corn"
            ]
        }
    ],
    "brinjal": [
        {
            "name": "Bacterial Wilt",
            "scientific_name": "Ralstonia solanacearum",
            "symptoms": ["Sudden wilting", "Browning of vascular tissue"],
            "chemical_treatment": "Streptocycline",
            "organic_treatment": "Bio-control with Pseudomonas fluorescens",
            "dosage": "1g per 10 liters",
            "recommendations": ["Ensure proper drainage", "Remove infected plants"]
        },
        {
            "name": "Phomopsis Blight",
            "scientific_name": "Phomopsis vexans",
            "symptoms": ["Circular brown spots", "Fruit rot"],
            "chemical_treatment": "Carbendazim 50% WP",
            "organic_treatment": "Trichoderma viride seed treatment",
            "dosage": "2g per liter",
            "recommendations": ["Improve plant spacing", "Remove affected parts"]
        },
        {
            "name": "Anthracnose",
            "scientific_name": "Colletotrichum gleosporioides",
            "chemical_treatment": "Mancozeb (2.5g/L) or Copper Oxychloride",
            "organic_treatment": "Neem oil spray (5ml/L)",
            "recommendations": ["Improve air circulation", "Remove infected fruits"]
        },
        {
            "name": "Little Leaf",
            "scientific_name": "Phytoplasma",
            "chemical_treatment": "None (Viral/Phytoplasma)",
            "organic_treatment": "Control leafhopper vectors with Neem oil",
            "recommendations": ["Remove and burn infected plants"]
        },
        {
            "name": "Powdery Mildew",
            "scientific_name": "Leveillula taurica",
            "chemical_treatment": "Wettable Sulfur (3g/L) or Dinocap",
            "organic_treatment": "Potassium bicarbonate spray",
            "recommendations": ["Decrease leaf moisture", "Remove lower infected leaves"]
        }
    ],
    "watermelon": [
        {
            "name": "Anthracnose",
            "scientific_name": "Colletotrichum orbiculare",
            "chemical_treatment": "Mancozeb or Chlorothalonil",
            "organic_treatment": "Copper-based fungicides or Neem oil",
            "dosage": "2g per liter, spray every 7-10 days",
            "recommendations": ["Avoid overhead irrigation", "Apply protective fungicides during wet weather"]
        },
        {
            "name": "Downy Mildew",
            "scientific_name": "Pseudoperonospora cubensis",
            "chemical_treatment": "Metalaxyl or Ridomil Gold",
            "organic_treatment": "Copper oxychloride",
            "dosage": "2.5g per liter",
            "recommendations": ["Improve plant spacing for air circulation"]
        },
        {
            "name": "Fusarium Wilt",
            "scientific_name": "Fusarium oxysporum",
            "chemical_treatment": "None (Soil-borne)",
            "organic_treatment": "Soil application of Trichoderma viride",
            "recommendations": ["Use resistant varieties", "Practice long-term crop rotation"]
        }
    ],
    "maize": [
        {
            "name": "Common Rust",
            "scientific_name": "Puccinia sorghi",
            "chemical_treatment": "Tilt (Propiconazole) or Follicur (Tebuconazole)",
            "organic_treatment": "Neem oil spray or sulfur-based dust",
            "dosage": "1ml per liter, apply upon first sign of pustules",
            "recommendations": ["Use resistant hybrids", "Plant early", "Manage humidity"]
        },
        {
            "name": "Gray Leaf Spot",
            "scientific_name": "Cercospora zeae-maydis",
            "chemical_treatment": "Headline (Pyraclostrobin) or Quilt Xcel",
            "organic_treatment": "Clean tillage",
            "dosage": "1.5ml per liter",
            "recommendations": ["Practice crop rotation", "Use resistant hybrids"]
        },
        {
            "name": "Northern Leaf Blight (TLB)",
            "scientific_name": "Exserohilum turcicum",
            "chemical_treatment": "Aproach (Picoxystrobin) or Stratego YLD",
            "organic_treatment": "Crop rotation to break cycle",
            "dosage": "2g per liter",
            "recommendations": ["Scout fields during silking", "Remove infected residue"]
        }
    ]
}
