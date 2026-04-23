import os
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers

# 1. Dataset Configuration
DATASET_PATH = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\maize_dataset"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

print("Loading Maize dataset for v9-Style High-Accuracy Training...")
# Classes: ['aspergillus_rot', 'common_rust', 'downy_mildew', 'gray_leaf_spot', 'healthy', 'northern_leaf_blight']
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='categorical'
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='categorical'
)

# 2. Preprocessing (MobileNetV2 standard [-1, 1])
normalization_layer = layers.Rescaling(1./127.5, offset=-1)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

# 3. Build Model (Replicating Brinjal v9 Logic)
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

# Deep unfreezing: Unfreeze top 100 layers for specialized feature extraction
base_model.trainable = True
for layer in base_model.layers[:-100]:
    layer.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.4),
    layers.Dense(6, activation='softmax')
])

# 4. Compile with v9-style precision learning rate
model.compile(
    optimizer=optimizers.Adam(learning_rate=2e-5),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 5. Manual Class Weights (Priority weighting for imbalanced Maize classes)
# Classes: aspergillus(0), rust(1), mildew(2), spot(3), healthy(4), blight(5)
class_weights = {
    0: 1.0,  # Aspergillus Rot
    1: 0.5,  # Common Rust (High count penalty)
    2: 5.0,  # Downy Mildew (MAX PRIORITY - only 30 images)
    3: 0.8,  # Gray Leaf Spot
    4: 2.0,  # Healthy (High priority for baseline)
    5: 0.8   # Northern Leaf Blight
}

# 6. Training (50 Epochs as per Brinjal v9)
print("Starting Maize v9-Style Deep Training (50 Epochs)...")
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=50,
    class_weight=class_weights,
    verbose=1
)

# 7. Save Model
model_path = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\app\ml\maize\maize_disease_v1.keras"
model.save(model_path)
print(f"Maize v9-style model saved to {model_path}")
