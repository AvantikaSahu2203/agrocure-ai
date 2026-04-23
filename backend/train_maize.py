import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

# --- CONFIGURATION ---
IMG_SIZE = 224
BATCH_SIZE = 16
DATASET_DIR = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\maize_dataset"
NUM_CLASSES = 6
SAVE_DIR = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\app\ml\maize"
SAVE_PATH = os.path.join(SAVE_DIR, "maize_disease_v1.keras")

# Explicit class order to ensure consistency between training runs
CLASS_NAMES = ["aspergillus_rot", "common_rust", "downy_mildew", "gray_leaf_spot", "healthy", "northern_leaf_blight"]

def train_maize_model():
    print("--- Preparing Maize Data Loaders (High Accuracy Mode) ---")
    
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # 1. Data Augmentation & Loading
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        rotation_range=30,
        zoom_range=0.2,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest'
    )

    train_data = train_datagen.flow_from_directory(
        DATASET_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        classes=CLASS_NAMES, # Force fixed order
        subset='training'
    )

    val_data = train_datagen.flow_from_directory(
        DATASET_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        classes=CLASS_NAMES, # Force fixed order
        subset='validation'
    )

    print(f"Detected Classes for Maize: {train_data.class_indices}")

    # Check if we should RESUME
    if os.path.exists(SAVE_PATH):
        print(f"\n--- FOUND EXISTING MODEL: {SAVE_PATH} ---")
        print("--- Resuming from Fine-Tuning Phase ---")
        try:
            model = tf.keras.models.load_model(SAVE_PATH)
            print("--- Model Loaded Successfully ---")
            skip_phase_1 = True
        except Exception as e:
            print(f"--- Failed to load existing model: {e}. Starting from scratch. ---")
            skip_phase_1 = False
    else:
        print("\n--- No existing model found. Starting full training pipeline. ---")
        skip_phase_1 = False

    if not skip_phase_1:
        # 2. Build High-Accuracy Architecture (EfficientNetB0)
        print("--- Building Optimized Maize Disease Architecture ---")
        base_model = tf.keras.applications.EfficientNetB0(
            input_shape=(IMG_SIZE, IMG_SIZE, 3),
            include_top=False,
            weights='imagenet'
        )
        
        base_model.trainable = False 

        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
            base_model,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(512, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
        ])

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        print("\n--- PHASE 1: Top Layer Calibration (5 Epochs) ---")
        model.fit(train_data, validation_data=val_data, epochs=5, verbose=1)
        
        # Save initial calibration
        model.save(SAVE_PATH)
    
    # 3. Fine-tuning Phase (Always run if we reached here)
    print("\n--- PHASE 2: Deep Fine-tuning (Unfreezing Backbone) ---")
    
    # Unfreeze the base model (it's the second layer in our Sequential model)
    # If we loaded the model, the structure is preserved.
    # Note: Accessing nested base model
    for layer in model.layers:
        if isinstance(layer, tf.keras.Model) or layer.name == 'efficientnetb0':
             layer.trainable = True
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # Optimization Callbacks
    early_stop = EarlyStopping(monitor='val_accuracy', patience=8, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_accuracy', factor=0.5, patience=3, min_lr=1e-7)
    checkpoint = ModelCheckpoint(SAVE_PATH, monitor='val_accuracy', save_best_only=True, mode='max')

    history = model.fit(
        train_data,
        validation_data=val_data,
        epochs=45,
        callbacks=[early_stop, reduce_lr, checkpoint],
        verbose=1
    )

    print(f"\n✅ TRAINING COMPLETE: High-accuracy Maize model saved to: {SAVE_PATH}")

if __name__ == "__main__":
    # Check if data exists before starting
    if os.path.exists(DATASET_DIR) and len(os.listdir(DATASET_DIR)) >= NUM_CLASSES:
        train_maize_model()
    else:
        print(f"❌ Error: Dataset directory {DATASET_DIR} not found or incomplete. Run download_maize.py first.")
