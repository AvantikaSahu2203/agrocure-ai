import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn.utils import class_weight

# --- CONFIGURATION (PRO-V3) ---
IMG_SIZE = 300  # EfficientNetB3 uses 300x300
BATCH_SIZE = 8  # Reduced batch size for larger model and resolution
DATASET_DIR = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\maize_dataset"
NUM_CLASSES = 6
SAVE_PATH = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\app\ml\maize\maize_disease_pro.keras"

CLASS_NAMES = ["aspergillus_rot", "common_rust", "downy_mildew", "gray_leaf_spot", "healthy", "northern_leaf_blight"]

def train_maize_pro():
    print("--- Preparing Pro Maize Data Loaders (Optimization Mode) ---")
    
    # 1. Advanced Augmentation Pipeline
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.7, 1.3],
        fill_mode='nearest'
    )

    train_data = train_datagen.flow_from_directory(
        DATASET_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        classes=CLASS_NAMES,
        subset='training',
        shuffle=True
    )

    val_data = train_datagen.flow_from_directory(
        DATASET_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        classes=CLASS_NAMES,
        subset='validation',
        shuffle=False
    )

    # 2. Calculate Class Weights (Crucial for Downy Mildew / Healthy imbalance)
    print("--- Calculating Class Weights for Imbalance Correction ---")
    labels = train_data.classes
    weights = class_weight.compute_class_weight(
        class_weight='balanced',
        classes=np.unique(labels),
        y=labels
    )
    class_weights_dict = dict(enumerate(weights))
    print(f"Computed Class Weights: {class_weights_dict}")

    # 3. Build Pro Architecture (EfficientNetB3 + Hybrid Head)
    print("--- Building Optimized EfficientNetB3 Architecture ---")
    base_model = tf.keras.applications.EfficientNetB3(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze backbone for Phase 1
    base_model.trainable = False 

    # Hybrid Pooling Head (Average + Max) for better sensitivity
    inputs = tf.keras.layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
    x = base_model(inputs)
    
    avg_pool = tf.keras.layers.GlobalAveragePooling2D()(x)
    max_pool = tf.keras.layers.GlobalMaxPooling2D()(x)
    concat = tf.keras.layers.Concatenate()([avg_pool, max_pool])
    
    x = tf.keras.layers.BatchNormalization()(concat)
    x = tf.keras.layers.Dense(512, activation='swish', kernel_regularizer=tf.keras.regularizers.l2(0.001))(x)
    x = tf.keras.layers.Dropout(0.5)(x)
    outputs = tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs)

    # Use Label Smoothing to prevent overconfidence in small data
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.1),
        metrics=['accuracy']
    )

    # 4. Phase 1: Warming up the Head (10 Epochs)
    print("\n--- PHASE 1: Head Calibration (10 Epochs) ---")
    model.fit(
        train_data, 
        validation_data=val_data, 
        epochs=10, 
        class_weight=class_weights_dict,
        verbose=1
    )

    # 5. Phase 2: Full Fine-tuning with Gradual Unfreezing Logic
    print("\n--- PHASE 2: Deep Fine-tuning (Full Unfreeze) ---")
    base_model.trainable = True
    
    # Recompile with very low LR for backbone stability
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=5e-5),
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.1),
        metrics=['accuracy']
    )

    # Callbacks for final optimization
    early_stop = EarlyStopping(monitor='val_accuracy', patience=12, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_accuracy', factor=0.3, patience=4, min_lr=1e-7)
    checkpoint = ModelCheckpoint(SAVE_PATH, monitor='val_accuracy', save_best_only=True, mode='max')

    print("--- Starting Final Optimization Run ---")
    model.fit(
        train_data,
        validation_data=val_data,
        epochs=60, # More epochs for B3 to converge
        class_weight=class_weights_dict,
        callbacks=[early_stop, reduce_lr, checkpoint],
        verbose=1
    )

    print(f"\nPRO TRAINING COMPLETE: Model saved to {SAVE_PATH}")

if __name__ == "__main__":
    train_maize_pro()
