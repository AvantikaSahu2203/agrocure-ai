import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# --- CONFIGURATION ---
IMG_SIZE = 224
BATCH_SIZE = 16
DATASET_DIR = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\watermelon_dataset"
NUM_CLASSES = 6

def train_watermelon_model():
    print("--- Preparing Watermelon Data Loaders ---")
    
    # Validation split 0.2
    # Aggressive augmentation to prevent overfitting on 100 images per class
    train_datagen = ImageDataGenerator(
        rescale=1./255,
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

    print(f"Classes found: {train_data.class_indices}")

    # Build EfficientNetB0 Architecture
    print("--- Building Optimized Watermelon Architecture ---")
    base_model = tf.keras.applications.EfficientNetB0(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    base_model.trainable = False # Initial warm-up

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    print("--- PHASE 1: Top Layer Calibration (5 Epochs) ---")
    model.fit(train_data, validation_data=val_data, epochs=5, verbose=2)

    print("--- PHASE 2: Deep Fine-tuning (Unfreezing All Layers) ---")
    base_model.trainable = True
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # Professional training callbacks
    early_stop = EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_accuracy', factor=0.5, patience=4, min_lr=1e-6)

    history = model.fit(
        train_data,
        validation_data=val_data,
        epochs=40,
        callbacks=[early_stop, reduce_lr],
        verbose=2
    )

    # Save the model
    save_dir = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\app\ml\watermelon"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    save_path = os.path.join(save_dir, "watermelon_disease_v1.keras")
    model.save(save_path)
    print(f"\n✅ SUCCESS: Watermelon model saved to: {save_path}")

if __name__ == "__main__":
    train_watermelon_model()
