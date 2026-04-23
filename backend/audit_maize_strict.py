import os
from PIL import Image
from pathlib import Path

def strict_audit(root_dir):
    print(f"--- Strict Audit: {root_dir} ---")
    root = Path(root_dir)
    removed_count = 0
    total_checked = 0
    
    for folder in root.iterdir():
        if not folder.is_dir():
            continue
            
        print(f"Checking folder: {folder.name}")
        for img_path in folder.iterdir():
            if img_path.is_file():
                total_checked += 1
                try:
                    with Image.open(img_path) as img:
                        img.verify() # Verify file integrity
                    # Re-open and verify format
                    with Image.open(img_path) as img:
                        if img.format not in ['JPEG', 'PNG', 'GIF', 'BMP', 'JPG']:
                            print(f"  [X] Illegal Format ({img.format}): {img_path.name}")
                            img_path.unlink()
                            removed_count += 1
                except Exception as e:
                    print(f"  [!] Corrupted/Unreadable: {img_path.name} - {e}")
                    img_path.unlink()
                    removed_count += 1
                    
    print(f"\nStrict Audit Complete.")
    print(f"Total checked: {total_checked}")
    print(f"Removed: {removed_count}")

if __name__ == "__main__":
    strict_audit(r"C:\Users\ASUS\Desktop\AgroCure AI\backend\maize_dataset")
