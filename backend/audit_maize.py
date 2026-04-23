import os
import cv2
from pathlib import Path

def audit_dataset(root_dir):
    print(f"--- Auditing Dataset: {root_dir} ---")
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
                    # Attempt to read the image
                    img = cv2.imread(str(img_path))
                    if img is None:
                        print(f"  [X] Corrupted/Invalid: {img_path.name}")
                        img_path.unlink()
                        removed_count += 1
                    else:
                        # Optional: check for zero dimensions
                        if img.shape[0] == 0 or img.shape[1] == 0:
                            print(f"  [X] Empty: {img_path.name}")
                            img_path.unlink()
                            removed_count += 1
                except Exception as e:
                    print(f"  [!] Error opening {img_path.name}: {e}")
                    img_path.unlink()
                    removed_count += 1
                    
    print(f"\nAudit Complete.")
    print(f"Total checked: {total_checked}")
    print(f"Removed: {removed_count}")

if __name__ == "__main__":
    audit_dataset(r"C:\Users\ASUS\Desktop\AgroCure AI\backend\maize_dataset")
