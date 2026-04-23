import os
import PIL
from PIL import Image

import os
import tensorflow as tf

dataset_dir = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\brinjal_rebuild_dataset"

def clean_dataset():
    print(f"--- Rigorous Cleaning dataset in {dataset_dir} ---")
    count_deleted = 0
    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Check extension
            ext = os.path.splitext(file)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.bmp']:
                print(f"Deleting unsupported/no extension file: {file_path}")
                os.remove(file_path)
                count_deleted += 1
                continue

            try:
                # Try to decode with TF
                img_raw = tf.io.read_file(file_path)
                img = tf.io.decode_image(img_raw, channels=3)
            except Exception as e:
                print(f"Deleting corrupted TF image: {file_path}")
                os.remove(file_path)
                count_deleted += 1
    
    print(f"--- Dataset cleaned. {count_deleted} invalid files removed. ---")

if __name__ == "__main__":
    clean_dataset()
