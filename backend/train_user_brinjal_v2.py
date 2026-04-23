import os
import shutil
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from bing_image_downloader import downloader

# --- CONFIGURATION ---
IMG_SIZE = 224
BATCH_SIZE = 16
DATASET_DIR = r"C:\Users\ASUS\Desktop\mobileapp\dataset_user\train"

# --- STEP 1: DOWNLOAD ROBUST DATASET ---
def setup_dataset():
    pass # Skipped due to Bing rate limits. Heavy augmentation used instead.

# --- STEP 2: HIGH-ACCURACY TRAINING ---
def train_model():
    print("--- Preparing Data Loaders ---")
    # Highly aggressive data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255, # Keep scaling consistent with inference
        validation_split=0.2,
        rotation_range=40,
        zoom_range=0.3,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    train_data = train_datagen.flow_from_directory(
        DATASET_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    val_data = train_datagen.flow_from_directory(
        DATASET_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    # Use EfficientNetB0 for superior accuracy-to-size ratio
    print("--- Building EfficientNetB0 Architecture ---")
    base_model = tf.keras.applications.EfficientNetB0(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze the base initially for a stable warm-up
    base_model.trainable = False

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(7, activation='softmax')
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    print("--- PHASE 1: Warm-up Training (Top Layers Only) ---")
    model.fit(train_data, validation_data=val_data, epochs=5, verbose=2)

    print("--- PHASE 2: Fine-tuning (Unfreezing Base Model) ---")
    base_model.trainable = True
    
    # Recompile with a much lower learning rate
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # Callbacks to prevent overfitting and hit 95%
    early_stop = EarlyStopping(monitor='val_accuracy', patience=8, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_accuracy', factor=0.5, patience=3, min_lr=1e-6)

    model.fit(
        train_data,
        validation_data=val_data,
        epochs=35, # Aggressive epochs since we have early stop
        callbacks=[early_stop, reduce_lr],
        verbose=2
    )

    save_path = r"C:\Users\ASUS\Desktop\AgroCure AI\backend\app\ml\brinjal\brinjal_disease_95_v2.keras"
    model.save(save_path)
    print(f"✅ Training Complete! Super-accurate model saved to: {save_path}")

if __name__ == "__main__":
    train_model()
