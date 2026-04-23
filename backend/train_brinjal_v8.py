import tensorflow as tf
from tensorflow.keras import layers, models, Sequential
import os

# Configuration
DATASET_DIR = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\brinjal_rebuild_dataset"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10 # Rapid convergence with transfer learning

def train_model():
    print("--- Loading Dataset ---")
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode='categorical'
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode='categorical'
    )

    class_names = train_ds.class_names
    print(f"Classes identified: {class_names}")

    def preprocess(image, label):
        image = image / 127.5 - 1.0
        return image, label

    train_ds = train_ds.map(preprocess)
    val_ds = val_ds.map(preprocess)

    # Optimize for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # Data Augmentation to help with noisy Bing data
    data_augmentation = Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.2),
    ])

    # Standard normalization for MobileNetV2: [-1, 1]
    normalization_layer = layers.Rescaling(1./127.5, offset=-1)

    # Base Model: MobileNetV2 (Pre-trained)
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Fine-tuning: Unfreeze the top layers
    base_model.trainable = True
    fine_tune_at = len(base_model.layers) - 30
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False

    # Build Top layers
    model = Sequential([
        layers.Input(shape=(224, 224, 3)),
        data_augmentation,
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.4),
        layers.Dense(len(class_names), activation='softmax')
    ])

    # Smaller learning rate for fine-tuning
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # Calculate class weights manually to handle imbalance
    print("--- Calculating Class Weights ---")
    counts = []
    for name in class_names:
        count = len(os.listdir(os.path.join(DATASET_DIR, name)))
        counts.append(count)
    
    total = sum(counts)
    class_weight_dict = {i: total / (len(class_names) * count) for i, count in enumerate(counts)}
    print(f"Class weights: {class_weight_dict}")

    # Early stopping
    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=5, # More patience for fine-tuning
        restore_best_weights=True
    )

    print("--- Starting Training (Fine-Tuning Mode) ---")
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=30, # Increased epochs
        class_weight=class_weight_dict,
        callbacks=[early_stop]
    )

    # Save
    model_path = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\app\ml\brinjal\brinjal_disease_model_v8.keras"
    model.save(model_path)
    print(f"Model successfully saved to {model_path}")

if __name__ == "__main__":
    from tensorflow.keras import Sequential
    train_model()
