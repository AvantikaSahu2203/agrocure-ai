import os
import time
from bing_image_downloader import downloader

# Configuration
DATASET_DIR = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\maize_dataset"
LIMIT = 150 # High-accuracy training requirement
MAX_RETRIES = 3
RETRY_DELAY = 10 # seconds

# Targeted classes for precise feature extraction 
# Optimized for higher reliability in automated scraping
CLASSES_MAP = {
    "common_rust": "maize leaf common rust",
    "gray_leaf_spot": "maize gray leaf spot leaf",
    "northern_leaf_blight": "maize northern leaf blight leaf",
    "healthy": "maize healthy leaf green",
    "aspergillus_rot": "maize aspergillus ear rot",
    "downy_mildew": "maize downy mildew leaf"
}

def download_maize_data():
    if not os.path.exists(DATASET_DIR):
        os.makedirs(DATASET_DIR)
        
    for folder_name, query in CLASSES_MAP.items():
        clean_folder = os.path.join(DATASET_DIR, folder_name)
        
        # SKIP if already complete
        if os.path.exists(clean_folder) and len(os.listdir(clean_folder)) >= LIMIT:
            print(f"--- Skipping {folder_name}: already has {len(os.listdir(clean_folder))} images ---")
            continue

        print(f"\n--- Scraping Dataset for: {folder_name} ({query}) ---")
        
        for attempt in range(MAX_RETRIES):
            try:
                downloader.download(
                    query, 
                    limit=LIMIT, 
                    output_dir=DATASET_DIR, 
                    adult_filter_off=True, 
                    force_replace=False,
                    timeout=60, 
                    verbose=True
                )
                success = True
                break
            except Exception as e:
                print(f"[WARNING] Attempt {attempt+1} failed for {folder_name}: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)

        # Merge raw downloaded folder into clean folder
        raw_folder = os.path.join(DATASET_DIR, query)
        if os.path.exists(raw_folder):
            if not os.path.exists(clean_folder):
                os.rename(raw_folder, clean_folder)
            else:
                for f in os.listdir(raw_folder):
                    src = os.path.join(raw_folder, f)
                    dst = os.path.join(clean_folder, f)
                    if not os.path.exists(dst):
                        try:
                            os.rename(src, dst)
                        except:
                            pass
                try:
                    import shutil
                    shutil.rmtree(raw_folder)
                except:
                    pass
                
    print(f"\n[SUCCESS] DATASET PREPARATION ATTEMPT COMPLETE")

if __name__ == "__main__":
    download_maize_data()
