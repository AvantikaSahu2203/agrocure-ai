import pandas as pd
import os

def check_distribution(csv_path: str):
    """
    Verify the dataset distribution against AgriNet-X requirements.
    Rules:
    - Healthy class < 40%
    - Multi-dataset mix (PV, Field, Mobile, synthetic)
    """
    if not os.path.exists(csv_path):
        print(f"Error: CSV not found at {csv_path}")
        return
        
    df = pd.read_csv(csv_path)
    total = len(df)
    print(f"Total Unified Images: {total}")
    
    # 1. Healthy Class Check
    healthy_mask = df['normalized_label'].str.contains('healthy', case=False, na=False)
    num_healthy = healthy_mask.sum()
    healthy_ratio = num_healthy / total
    print(f"Healthy class: {num_healthy} ({healthy_ratio*100:.2f}%)")
    
    if healthy_ratio > 0.40:
        print("!! WARNING: Healthy bias detected (>40%). Need to balance.")
    else:
        print("✔ Healthy ratio within safe limits (<40%).")
        
    # 2. Dataset Source Check
    print("\nDataset Distribution:")
    dist = df['dataset'].value_counts(normalize=True)
    for source, ratio in dist.items():
        print(f"- {source}: {ratio*100:.2f}%")
        
    # 3. Class Imbalance (Rare Diseases)
    print("\nRare Disease Classes (top 5 smallest):")
    counts = df['normalized_label'].value_counts()
    print(counts.tail(5))

if __name__ == "__main__":
    # Check current unified dataset
    PATH = "../../dataset_unified/unified_metadata.csv"
    check_distribution(PATH)
