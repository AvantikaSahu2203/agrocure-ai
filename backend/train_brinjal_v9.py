import os
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
import matplotlib.pyplot as plt

# 1. Dataset Configuration
DATASET_PATH = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\brinjal_rebuild_dataset"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

print("Loading datasets for v9 High-Accuracy Training...")
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

# 2. Preprocessing (MobileNetV2 [-1, 1])
normalization_layer = layers.Rescaling(1./127.5, offset=-1)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

# 3. Build Model (Deep Fine-Tuning v9)
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
    layers.Dense(7, activation='softmax')
])

# 4. Compile with precision LR
model.compile(
    optimizer=optimizers.Adam(learning_rate=2e-5),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 5. Class Weights (Addressing imbalance reported by user)
# Counts: Aphid(87), Wilt(106), Healthy(138), Leaf(31), Phomopsis(84), Mite(28), TMV(98)
# We prioritize Mite (28) and Leaf (31) to fix the Phomopsis bias
class_weights = {
    0: 1.0,  # Bacterial Wilt
    1: 1.0,  # Aphid
    2: 0.8,  # Healthy (Lower weight to reduce false negatives)
    3: 3.0,  # Little Leaf (HIGH PRIORITY)
    4: 1.0,  # Phomopsis Blight
    5: 3.5,  # Spider Mite (MAX PRIORITY)
    6: 1.0   # Tobacco Mosaic Virus
}

# 6. Training
print("Starting v9 Deep Retraining (50 Epochs)...")
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=50,
    class_weight=class_weights
)

# 7. Save Model
model_path = r"c:\Users\ASUS\Desktop\AgroCure AI\backend\app\ml\brinjal\brinjal_disease_model_v9.keras"
model.save(model_path)
print(f"v9 Model saved to {model_path}")
