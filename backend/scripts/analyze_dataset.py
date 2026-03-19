import pandas as pd
import os

metadata_path = r'c:\Users\ASUS\Desktop\AgroCure AI\backend\dataset_unified\unified_metadata.csv'
if os.path.exists(metadata_path):
    df = pd.read_csv(metadata_path)
    counts = df['normalized_label'].value_counts()
    with open('dataset_analysis.txt', 'w') as f:
        f.write("Label Counts:\n")
        f.write(counts.to_string())
        
        # Check for the 4 target classes
        targets = ['Healthy', 'Blight', 'Powdery_Mildew', 'Leaf_Spot']
        for target in targets:
            matches = [idx for idx in counts.index if target.lower() in idx.lower()]
            f.write(f"\n\nMatches for {target}:\n")
            f.write(df[df['normalized_label'].isin(matches)]['normalized_label'].value_counts().to_string())
    print("Analysis saved to dataset_analysis.txt")
else:
    print(f"File not found: {metadata_path}")
