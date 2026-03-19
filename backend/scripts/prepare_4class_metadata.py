import os
import pandas as pd

def prepare_4class_metadata():
    base_dir = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\downloads\megaplant_subset_extracted"
    output_csv = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\dataset_unified\train_metadata_v7.csv"
    
    data = []
    
    # 0: Healthy, 1: Blight, 2: Powdery Mildew, 3: Leaf Spot
    mapping = {
        "healthy": 0,
        "blight": 1,
        "powdery_mildew": 2,
        "spot": 3,
        "scab": 3,
        "scorch": 3,
        "leaf_spot": 3
    }
    
    # 1. Process PlantVillage & PlantDoc (Same structure)
    for source in ["plantvillage", "plantdoc"]:
        src_dir = os.path.join(base_dir, source)
        if not os.path.exists(src_dir):
            continue
            
        print(f"Processing {source}...")
        # Healthy
        h_dir = os.path.join(src_dir, "healthy")
        if os.path.exists(h_dir):
            for f in os.listdir(h_dir):
                if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                    rel_path = os.path.relpath(os.path.join(h_dir, f), r"c:\Users\ASUS\Desktop\AgroCure AI\backend\dataset_unified")
                    data.append({"image_path": rel_path, "target_label": 0})
        
        # Unhealthy
        u_dir = os.path.join(src_dir, "unhealthy")
        if os.path.exists(u_dir):
            for sub in os.listdir(u_dir):
                if sub in mapping:
                    label = mapping[sub]
                    sub_path = os.path.join(u_dir, sub)
                    for f in os.listdir(sub_path):
                        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                             rel_path = os.path.relpath(os.path.join(sub_path, f), r"c:\Users\ASUS\Desktop\AgroCure AI\backend\dataset_unified")
                             data.append({"image_path": rel_path, "target_label": label})

    df = pd.DataFrame(data)
    print(f"Total samples found so far: {len(df)}")
    if len(df) > 0:
        print("Class distribution:")
        print(df['target_label'].value_counts())
        df.to_csv(output_csv, index=False)
        print(f"Metadata saved to {output_csv}")

if __name__ == "__main__":
    prepare_4class_metadata()
