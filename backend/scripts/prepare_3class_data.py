import pandas as pd
import os

def prepare_3class_data():
    unified_csv = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\dataset_unified\unified_metadata.csv"
    output_csv = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\dataset_unified\train_metadata_v7_temp.csv"
    
    if not os.path.exists(unified_csv):
        print(f"Error: {unified_csv} not found.")
        return
        
    df = pd.read_csv(unified_csv)
    
    # Define mapping to targets: 0: Healthy, 1: Blight, 2: Powdery Mildew, 3: Leaf Spot
    def map_label(label):
        label_lower = label.lower()
        if "healthy" in label_lower:
            return 0
        elif "blight" in label_lower:
            return 1
        elif "mildew" in label_lower:
            return 2
        elif "spot" in label_lower or "scab" in label_lower or "scorch" in label_lower:
            return 3
        return -1 # Unmapped
        
    df['target_label'] = df['normalized_label'].apply(map_label)
    
    # Filter out unmapped (like Mite Damage, Viral Mosaic if they don't fit)
    filtered_df = df[df['target_label'] != -1].copy()
    
    print(f"Original samples: {len(df)}")
    print(f"Mapped samples: {len(filtered_df)}")
    print("Class distribution:")
    print(filtered_df['target_label'].value_counts())
    
    filtered_df.to_csv(output_csv, index=False)
    print(f"Metadata saved to {output_csv}")

if __name__ == "__main__":
    prepare_3class_data()
