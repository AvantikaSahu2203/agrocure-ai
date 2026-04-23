import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image

model_path = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\app\ml\brinjal\brinjal_disease_model_v8.keras"
dataset_dir = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\brinjal_rebuild_dataset"

def verify():
    print(f"--- Verifying Model: {model_path} ---")
    model = tf.keras.models.load_model(model_path)
    
    # The folders in directory order (alphabetical)
    class_names = sorted([d for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))])
    print(f"Target Sequence: {class_names}")

    correct = 0
    total = 0

    for i, class_name in enumerate(class_names):
        class_dir = os.path.join(dataset_dir, class_name)
        images = [f for f in os.listdir(class_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if not images:
            continue
            
        test_img_path = os.path.join(class_dir, images[0])
        
        img = image.load_img(test_img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Standard MobileNetV2 preprocessing: [-1, 1]
        img_array = img_array / 127.5 - 1.0
        
        prediction = model.predict(img_array, verbose=0)
        predicted_idx = np.argmax(prediction)
        predicted_class = class_names[predicted_idx]
        
        print(f"Folder: {class_name[:20]}... | Predicted: {predicted_class[:20]}... | {'CORRECT' if predicted_idx == i else 'WRONG'}")
        
        if predicted_idx == i:
            correct += 1
        total += 1

    print(f"--- Verification Summary: {correct}/{total} correct on sample set ---")

if __name__ == "__main__":
    verify()
