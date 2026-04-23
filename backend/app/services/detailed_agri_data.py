# Regional ICAR-based growth stage protocols for standard Indian crops

CROP_STAGES = {
    "Rice": {
        "Seedling": {
            "fertilizer": "NPK 14:14:14 @ 50kg/ha during transplanting.",
            "irrigation": "Keep 2-3cm water depth in the nursery.",
            "spray": "Treat seeds with Carbendazim (2g/kg)."
        },
        "Vegetative": {
            "fertilizer": "Top dress with Urea (25kg/ha) 20 days after transplanting.",
            "irrigation": "Maintain 5cm water level; Alternate Wetting and Drying (AWD) recommended.",
            "spray": "Spray Neem oil (3ml/L) if Leaf folder is observed."
        },
        "Flowering": {
            "fertilizer": "Apply Muriate of Potash (MOP) @ 15kg/ha.",
            "irrigation": "Most critical stage: Never let the field dry.",
            "spray": "Spray Boron (1g/L) to prevent grain sterility."
        },
        "Harvest": {
            "fertilizer": "No application required.",
            "irrigation": "Drain field 10-15 days before harvest.",
            "spray": "Stop all chemical pesticides."
        }
    },
    "Brinjal": {
        "Seedling": {
            "fertilizer": "Mix well-rotted FYM (10t/ha) in soil.",
            "irrigation": "Light watering using rose can every morning.",
            "spray": "Drench with Captan (0.2%) to prevent damping-off."
        },
        "Vegetative": {
            "fertilizer": "Apply 50kg Nitrogen/ha in two split doses.",
            "irrigation": "Irrigate at 7-10 day intervals.",
            "spray": "Monitor for Shoot & Fruit Borer; use Pheromone traps."
        },
        "Flowering": {
            "fertilizer": "Spray NAA (20ppm) to prevent flower drop.",
            "irrigation": "Maintain consistent moisture.",
            "spray": "Spray Spinosad for Borer control."
        },
        "Harvest": {
            "fertilizer": "Top dress with 25kg N after every 3-4 pickings.",
            "irrigation": "Irrigate after every harvest to help next fruit set.",
            "spray": "Observe 7-day safety period before picking."
        }
    },
    "Tomato": {
        "Seedling": {
            "fertilizer": "DAP @ 10g/sq.m in nursery bed.",
            "irrigation": "Maintain field capacity moisture.",
            "spray": "Protect against Whitefly with yellow sticky traps."
        },
        "Vegetative": {
            "fertilizer": "Side-dress Nitrate of Soda @ 15kg/ha.",
            "irrigation": "Regular irrigation, especially during dry spells.",
            "spray": "Spray Copper Oxychloride for Early Blight prevention."
        },
        "Flowering": {
            "fertilizer": "Apply Potash for fruit quality.",
            "irrigation": "Ensure no drought stress; results in blossom end rot.",
            "spray": "Spray Calcium Nitrate (0.5%) for fruit firmness."
        },
        "Harvest": {
            "fertilizer": "N/A",
            "irrigation": "Avoid excessive watering as fruits mature (cracking risk).",
            "spray": "N/A"
        }
    },
    "Watermelon": {
        "Seedling": {
            "fertilizer": "Basal dose of N:P:K 40:40:40 kg/ha.",
            "irrigation": "Drip irrigation recommended from day 1.",
            "spray": "Protect against Red Pumpkin Beetle."
        },
        "Vegetative": {
            "fertilizer": "Apply remaining 40kg Nitrogen at 30 days.",
            "irrigation": "Once in 3 days; avoid wetting leaves.",
            "spray": "Focus on Downy Mildew prevention in humid weather."
        },
        "Flowering": {
            "fertilizer": "Apply Borax (10kg/ha) for fruit set.",
            "irrigation": "Regular watering to ensure fruit size.",
            "spray": "Keep beehives nearby or avoid evening sprays to boost pollination."
        },
        "Harvest": {
            "fertilizer": "N/A",
            "irrigation": "Reduce watering significantly (increases sugar content).",
            "spray": "N/A"
        }
    },
    "Maize": {
        "Seedling": {
            "fertilizer": "Apply 30-40kg Nitrogen and full dose of P & K at sowing.",
            "irrigation": "Provide light irrigation immediately after sowing.",
            "spray": "Treat seeds with Thiram (2g/kg) to prevent fungal wilt."
        },
        "Vegetative": {
            "fertilizer": "Side-dress with 40kg Nitrogen at knee-high stage.",
            "irrigation": "Most sensitive stage; ensure no waterlogging.",
            "spray": "Monitor for Fall Armyworm; use Neem-based sprays if needed."
        },
        "Flowering": {
            "fertilizer": "Apply Potash for grain filling and cob strength.",
            "irrigation": "Critical for pollination; maintain soil moisture.",
            "spray": "Spray 2% Urea at tasseling for improved yield."
        },
        "Harvest": {
            "fertilizer": "N/A.",
            "irrigation": "Drain field when silks turn brown and kernels dry.",
            "spray": "Safe harvesting when moisture is below 20%."
        }
    }
}

# Default generic fallback for other crops
DEFAULT_STAGES = {
    "Seedling": {
        "fertilizer": "Apply light starter NPK.",
        "irrigation": "Keep soil moist but not soggy.",
        "spray": "Preventive fungal drenching."
    },
    "Vegetative": {
        "fertilizer": "Apply Nitrogen-rich fertilizer for leaf growth.",
        "irrigation": "Weekly irrigation or as per soil dryness.",
        "spray": "Monitor for common pests like Aphids."
    },
    "Flowering": {
        "fertilizer": "Apply Phosphorous and Potash.",
        "irrigation": "Ensure steady moisture during bloom.",
        "spray": "Preventive sprays for flower blight."
    },
    "Harvest": {
        "fertilizer": "None.",
        "irrigation": "Reduce watering.",
        "spray": "Respect pre-harvest intervals."
    }
}
