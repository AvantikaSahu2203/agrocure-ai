import zipfile
import os
import shutil

def zip_app_folder():
    print("--- Preparing AgroCure Deployment ZIP ---")
    zip_name = 'app.zip'
    folder_to_zip = 'app'
    
    if os.path.exists(zip_name):
        print(f"Removing old {zip_name}...")
        os.remove(zip_name)
    
    print(f"Creating new {zip_name} from '{folder_to_zip}' folder...")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_to_zip):
            # Skip pycache
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')
            
            for file in files:
                file_path = os.path.join(root, file)
                # Use relative path for zip entry
                arcname = file_path
                zipf.write(file_path, arcname)
    
    print(f"SUCCESS: {zip_name} is ready for deployment.")
    print("Next step: Upload this file and your updated backend files to Hugging Face.")

if __name__ == "__main__":
    zip_app_folder()
