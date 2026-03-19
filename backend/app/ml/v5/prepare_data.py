import pandas as pd
import os
import json
from sklearn.model_selection import train_test_split

def prepare_v5_data(csv_path, output_dir):
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # 1. Parse labels
    # Format is usually Crop__Disease. Some might be just Crop__Healthy
    df['crop'] = df['normalized_label'].apply(lambda x: x.split('__')[0] if '__' in x else x)
    df['disease'] = df['normalized_label'].apply(lambda x: x.split('__')[1] if '__' in x else 'Healthy')
    
    # 2. Create Mappings
    crops = sorted(df['crop'].unique())
    diseases = sorted(df['normalized_label'].unique()) # Using full normalized label for disease head is safer
    
    crop_map = {name: i for i, name in enumerate(crops)}
    disease_map = {name: i for i, name in enumerate(diseases)}
    
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, 'crop_map.json'), 'w') as f:
        json.dump(crop_map, f, indent=4)
    with open(os.path.join(output_dir, 'disease_map.json'), 'w') as f:
        json.dump(disease_map, f, indent=4)
        
    print(f"Mappings saved. Crops: {len(crops)}, Diseases: {len(diseases)}")
    
    # 3. Assign IDs
    df['crop_id'] = df['crop'].map(crop_map)
    df['disease_id'] = df['normalized_label'].map(disease_map)
    df['severity'] = 0.5 # Mock severity if not in CSV
    
    # 4. Split
    train_df, val_df = train_test_split(df, test_size=0.15, stratify=df['normalized_label'], random_state=42)
    
    train_df.to_csv(os.path.join(output_dir, 'train.csv'), index=False)
    val_df.to_csv(os.path.join(output_dir, 'val.csv'), index=False)
    
    print(f"Data split saved. Train size: {len(train_df)}, Val size: {len(val_df)}")

if __name__ == "__main__":
    csv_path = "backend/dataset_unified/unified_metadata.csv"
    output_dir = "backend/app/ml/v5/data"
prepare_v5_data(csv_path, output_dir)
