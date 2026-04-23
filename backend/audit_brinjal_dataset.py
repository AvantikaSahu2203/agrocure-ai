import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image

model_path = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\app\ml\brinjal\brinjal_disease_model_v8.keras"
dataset_dir = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\brinjal_rebuild_dataset"

def audit():
    print(f"--- Full Dataset Audit: {model_path} ---")
    model = tf.keras.models.load_model(model_path)
    
    class_names = sorted([d for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))])
    
    matrix = np.zeros((len(class_names), len(class_names)), dtype=int)
    
    for i, true_class in enumerate(class_names):
        print(f"Auditing class: {true_class}...")
        class_dir = os.path.join(dataset_dir, true_class)
        images = [f for f in os.listdir(class_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        for img_name in images:
            img_path = os.path.join(class_dir, img_name)
            try:
                img = image.load_img(img_path, target_size=(224, 224))
                x = image.img_to_array(img)
                x = np.expand_dims(x, axis=0)
                x = x / 127.5 - 1.0 # Normalization
                
                preds = model.predict(x, verbose=0)
                pred_idx = np.argmax(preds[0])
                matrix[i][pred_idx] += 1
            except:
                continue

    print("\n--- Confusion Matrix (True Class = Rows, Predicted = Cols) ---")
    header = " " * 25
    for j in range(len(class_names)):
        header += f"[{j}] "
    print(header)
    
    for i, row in enumerate(matrix):
        row_str = f"{class_names[i][:20]:<25}"
        for val in row:
            row_str += f"{val:<4}"
        print(row_str)

    print("\n--- Key Mapping ---")
    for i, name in enumerate(class_names):
        print(f"[{i}] {name}")

if __name__ == "__main__":
    audit()
