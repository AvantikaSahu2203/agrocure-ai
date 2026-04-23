import os
import shutil
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from bing_image_downloader import downloader

# --- STEP 1: DOWNLOAD DATA (EXACT QUERIES FROM CELL 14) ---
def setup_dataset():
    base_dir = "dataset_user"
    train_dir = os.path.join(base_dir, "train")
    os.makedirs(train_dir, exist_ok=True)
    
    queries = {
        "anthracnose": "brinjal anthracnose fruit lesions",
        "bacterial_wilt": "brinjal bacterial wilt leaf symptoms close up",
        "brinjal_healthy": "healthy brinjal leaf close up",
        "little_leaf": "brinjal little leaf disease symptoms",
        "phomopsis_blight": "brinjal phomopsis blight leaf spot",
        "powdery_mildew": "brinjal powdery mildew white powder leaf",
        "verticillium_wilt": "brinjal verticillium wilt yellow leaf"
    }
    
    for class_name, query in queries.items():
        print(f"--- Downloading {class_name} ---")
        downloader.download(
            query,
            limit=45, # Slightly more for buffer
            output_dir=train_dir,
            adult_filter_off=True,
            force_replace=False,
            timeout=60
        )
        # Move files from query-named folder to class-named folder
        query_folder = os.path.join(train_dir, query)
        class_folder = os.path.join(train_dir, class_name)
        
        if os.path.exists(query_folder):
            if not os.path.exists(class_folder):
                os.makedirs(class_folder)
            for file in os.listdir(query_folder):
                shutil.move(os.path.join(query_folder, file), os.path.join(class_folder, file))
            shutil.rmtree(query_folder)

# --- STEP 2: TRAINING LOGIC (EXACT STEPS FROM CELL 24) ---
def train_model():
    img_size = 224
    batch_size = 16
    dataset_path = "dataset_user/train"

    # DATA AUGMENTATION
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        rotation_range=20,
        zoom_range=0.2,
        horizontal_flip=True,
        shear_range=0.2
    )

    train_data = train_datagen.flow_from_directory(
        dataset_path,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )

    val_data = train_datagen.flow_from_directory(
        dataset_path,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )

    # MODEL ARCHITECTURE
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224,224,3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = True

    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(7, activation='softmax')
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    print("--- Starting Training (15 Epochs) ---")
    model.fit(
        train_data,
        validation_data=val_data,
        epochs=15,
        verbose=2 # Avoid unicode progress bar errors on Windows console
    )

    save_path = r"C:\Users\ASUS\Desktop\AgroCure AI\backend\app\ml\brinjal\brinjal_disease_model_user.keras"
    model.save(save_path)
    print(f"✅ Local Re-Bake Complete! Model saved to: {save_path}")

if __name__ == "__main__":
    # Skipping download as it's already complete
    # setup_dataset() 
    train_model()
