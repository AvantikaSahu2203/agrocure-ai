import os
from huggingface_hub import snapshot_download

def download_megaplant():
    repo_id = "chrisandrei/MegaPlant"
    local_dir = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\downloads\megaplant"
    
    print(f"Downloading MegaPlant dataset from Hugging Face ({repo_id})...")
    
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
        
    try:
        # Download the dataset
        path = snapshot_download(
            repo_id=repo_id,
            repo_type="dataset",
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )
        print(f"Dataset downloaded successfully to: {path}")
    except Exception as e:
        print(f"Error downloading dataset: {e}")

if __name__ == "__main__":
    download_megaplant()
