import os
import pandas as pd
from PIL import Image
import hashlib

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def find_disease_folders(root_dir):
    """
    Finds folders that directly contain images, assuming these are the disease classes.
    """
    disease_folders = []
    for root, dirs, files in os.walk(root_dir):
        # Check if current folder has images
        if any(f.lower().endswith(('.jpg', '.jpeg', '.png')) for f in files):
            disease_folders.append(root)
    return disease_folders

def unify_dataset(src_dir, dataset_name, crop_name, unified_dir, metadata_path):
    """
    Processes images from src_dir, resizes to 256x256, copies to unified_dir/images,
    and updates metadata_path.
    """
    if not os.path.exists(os.path.join(unified_dir, 'images')):
        os.makedirs(os.path.join(unified_dir, 'images'))

    # Load existing metadata
    if os.path.exists(metadata_path):
        df = pd.read_csv(metadata_path)
    else:
        df = pd.DataFrame(columns=['image_path', 'raw_label', 'normalized_label', 'dataset', 'hash'])

    new_entries = []
    
    # Find folders containing images
    disease_paths = find_disease_folders(src_dir)
    
    for class_path in disease_paths:
        class_name = os.path.basename(class_path)
        print(f"Processing {crop_name} - {class_name}...")
        
        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            if not img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
                
            try:
                # Open and check resolution
                with Image.open(img_path) as img:
                    img = img.convert('RGB')
                    if img.size != (256, 256):
                        img = img.resize((256, 256), Image.LANCZOS)
                    
                    # Target filename - include folder name to avoid collisions
                    target_name = f"{dataset_name}_{class_name.replace(' ', '_')}_{img_name.split('.')[0]}.JPG"
                    target_path = os.path.join(unified_dir, 'images', target_name)
                    
                    # Save
                    img.save(target_path, "JPEG")
                    
                    # Metadata
                    img_hash = get_file_hash(target_path)
                    new_entries.append({
                        'image_path': os.path.join('images', target_name),
                        'raw_label': f"{crop_name}__{class_name}",
                        'normalized_label': f"{crop_name}__{class_name.replace(' ', '_')}",
                        'dataset': dataset_name,
                        'hash': img_hash
                    })
            except Exception as e:
                print(f"Error processing {img_name}: {e}")

    # Append and save
    if new_entries:
        new_df = pd.DataFrame(new_entries)
        # Avoid hash collisions and duplicates
        df = pd.concat([df, new_df], ignore_index=True)
        df = df.drop_duplicates(subset=['hash'])
        df.to_csv(metadata_path, index=False)
        print(f"Successfully added {len(new_entries)} images to {metadata_path}")
    else:
        print(f"No images found for {crop_name} in {src_dir}")

if __name__ == "__main__":
    UNIFIED_ROOT = r'c:\Users\ASUS\Desktop\AgroCure AI\backend\dataset_unified'
    METADATA = os.path.join(UNIFIED_ROOT, 'unified_metadata.csv')
    DOWNLOADS_ROOT = r'c:\Users\ASUS\Desktop\AgroCure AI\backend\downloads'
    
    # Updated mappings to handle potential varied folder names
    # (search_pattern, dataset_alias, crop_name)
    MAPPINGS = [
        ('corn', 'CornKaggle', 'Corn'),
        ('rice', 'RiceKaggle', 'Rice'),
        ('cotton', 'CottonKaggle', 'Cotton')
    ]
    
    for pattern, d_name, crop in MAPPINGS:
        # Simple pattern matching to find folder
        found = False
        for folder in os.listdir(DOWNLOADS_ROOT):
            if pattern.lower() in folder.lower() and os.path.isdir(os.path.join(DOWNLOADS_ROOT, folder)):
                folder_path = os.path.join(DOWNLOADS_ROOT, folder)
                unify_dataset(folder_path, d_name, crop, UNIFIED_ROOT, METADATA)
                found = True
        if not found:
            print(f"Dataset for {crop} (pattern '{pattern}') not found in {DOWNLOADS_ROOT}")
