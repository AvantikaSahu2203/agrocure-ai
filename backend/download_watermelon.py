import os
from bing_image_downloader import downloader

# Configuration
DATASET_DIR = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\watermelon_dataset"
LIMIT = 100 # Balanced count for initial high-accuracy training

# Classes mapped to specific search queries for high quality
CLASSES = [
    "watermelon anthracnose leaf spots",
    "watermelon fusarium wilt symptoms",
    "watermelon downy mildew yellow spots",
    "watermelon powdery mildew white powder",
    "watermelon mosaic virus patterns",
    "watermelon leaf healthy"
]

def download_data():
    if not os.path.exists(DATASET_DIR):
        os.makedirs(DATASET_DIR)
        
    for query in CLASSES:
        print(f"\n--- Downloading: {query} ---")
        # Ensure subfolder naming is clean for the training loader
        folder_name = query.replace(" ", "_").replace("watermelon_", "")
        
        downloader.download(
            query, 
            limit=LIMIT, 
            output_dir=DATASET_DIR, 
            adult_filter_off=True, 
            force_replace=False, 
            timeout=60, 
            verbose=True
        )

if __name__ == "__main__":
    download_data()
