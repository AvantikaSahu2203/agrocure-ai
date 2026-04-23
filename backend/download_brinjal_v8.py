import os
from bing_image_downloader import downloader

# Configuration
DATASET_DIR = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\brinjal_rebuild_dataset"
LIMIT = 100 # Images per class for rapid rebuilding

# Exact sequence as requested for mapping alignment
CLASSES = [
    "brinjal leaf aphids",
    "brinjal bacterial wilt",
    "brinjal little leaf disease",
    "brinjal phomopsis blight",
    "brinjal spider mite damage",
    "brinjal tobacco mosaic virus",
    "brinjal leaf healthy"
]

def download_data():
    if not os.path.exists(DATASET_DIR):
        os.makedirs(DATASET_DIR)
        
    for query in CLASSES:
        print(f"\n--- Downloading: {query} ---")
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
