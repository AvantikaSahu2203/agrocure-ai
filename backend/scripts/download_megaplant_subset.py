import os
from huggingface_hub import hf_hub_download

def download_subset():
    repo_id = "chrisandrei/MegaPlant"
    local_dir = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\downloads\megaplant_subset"
    
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
        
    files_to_download = ["plantvillage.zip", "plantdoc.zip"]
    
    for filename in files_to_download:
        print(f"Downloading {filename}...")
        try:
            path = hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                repo_type="dataset",
                local_dir=local_dir,
                local_dir_use_symlinks=False
            )
            print(f"Downloaded {filename} to {path}")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")

if __name__ == "__main__":
    download_subset()
