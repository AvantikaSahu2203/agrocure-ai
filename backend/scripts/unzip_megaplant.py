import os
import zipfile

def unzip_megaplant():
    download_dir = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\downloads\megaplant_subset"
    extract_dir = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\downloads\megaplant_subset_extracted"
    
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)
        
    zips = [f for f in os.listdir(download_dir) if f.endswith('.zip')]
    
    for zip_name in zips:
        zip_path = os.path.join(download_dir, zip_name)
        print(f"Extracting {zip_name}...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            print(f"Finished extracting {zip_name}")
        except Exception as e:
            print(f"Error extracting {zip_name}: {e}")

if __name__ == "__main__":
    unzip_megaplant()
