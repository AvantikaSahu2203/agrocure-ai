import pandas as pd
import torch
from tqdm import tqdm
import os

def find_hard_examples(csv_path, model_engine, output_csv="hard_examples.csv"):
    """
    Identifies 'Diseased' images that the model incorrectly labels as 'Healthy'.
    """
    df = pd.read_csv(csv_path)
    hard_examples = []
    
    print(f"Analyzing {len(df)} images for false healthy predictions...")
    
    for _, row in tqdm(df.iterrows(), total=len(df)):
        img_path = row['image_path']
        label = row['normalized_label']
        
        # We only care about images that ARE diseased
        if "healthy" in label.lower():
            continue
            
        full_path = os.path.join("backend/dataset_unified", img_path)
        if not os.path.exists(full_path):
            continue
            
        with open(full_path, "rb") as f:
            img_bytes = f.read()
            
        # Run prediction
        try:
            pred = model_engine.predict(img_bytes)
            # Check if model says Healthy
            if pred.get("status") == "Healthy" or "healthy" in pred.get("disease_name", "").lower():
                hard_examples.append({
                    "image_path": img_path,
                    "true_label": label,
                    "predicted": pred.get("disease_name"),
                    "binary_logit": pred.get("binary_logit")
                })
        except Exception as e:
            continue
            
    if hard_examples:
        hard_df = pd.DataFrame(hard_examples)
        hard_df.to_csv(output_csv, index=False)
        print(f"Found {len(hard_examples)} hard examples. Saved to {output_csv}")
    else:
        print("No hard examples found in the current batch.")

if __name__ == "__main__":
    # This would be run in a production environment with the actual model loaded
    print("Hard Example Mining Utility Ready.")
