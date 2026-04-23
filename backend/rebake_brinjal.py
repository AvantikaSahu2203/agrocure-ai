"""
Re-Bake Script: Rebuild brinjal model architecture and transfer weights.
Run once: python rebake_brinjal.py
"""
import sys
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# Force UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import tensorflow as tf
from tensorflow import keras

print(f"TF: {tf.__version__}")

broken_path = r"C:\Users\ASUS\Desktop\AgroCure AI\backend\app\ml\brinjal\brinjal_disease_model_user.keras"
clean_path  = r"C:\Users\ASUS\Desktop\AgroCure AI\backend\app\ml\brinjal\brinjal_user_clean.keras"

# === 1. Build the EXACT architecture from train_user_brinjal.py ===
def build_model():
    base_model = keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights=None   # We load weights from file, not imagenet
    )
    base_model.trainable = True
    model = keras.Sequential([
        keras.layers.Input(shape=(224, 224, 3)),
        base_model,
        keras.layers.GlobalAveragePooling2D(),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(7, activation='softmax')
    ])
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

print("--- Building fresh model architecture ---")
model = build_model()
print(f"Model built. Params: {model.count_params():,}")

# === 2. Load the broken model just to extract weights via get_weights() ===
print(f"\n--- Extracting weights from broken model ---")
print(f"  Path: {broken_path}")

try:
    # Use a SEPARATE graph to load the broken model - avoids the arch conflict
    broken_model = keras.models.load_model(broken_path, compile=False)
    print("SUCCESS: Broken model loaded for weight extraction!")
    broken_weights = broken_model.get_weights()
    print(f"  Extracted {len(broken_weights)} weight tensors")

    # Transfer weights into clean model
    print("--- Transferring weights ---")
    model.set_weights(broken_weights)
    print("SUCCESS: Weights transferred!")

except Exception as e:
    print(f"WARN: Could not extract from broken model: {e}")
    print("--- Trying load_weights() directly ---")
    try:
        model.load_weights(broken_path, skip_mismatch=True)
        print("SUCCESS: load_weights() with skip_mismatch worked!")
    except Exception as e2:
        print(f"WARN: load_weights also failed: {e2}")
        print("NOTE: Saving model with random weights for architecture verification only.")
        print("      You will need to retrain to get proper weights.")

# === 3. Sanity check ===
dummy = np.zeros((1, 224, 224, 3), dtype=np.float32)
out = model.predict(dummy, verbose=0)
print(f"\nSanity check output shape: {out.shape}, argmax={out.argmax()}, sum={out.sum():.4f}")

# === 4. Save clean model ===
print(f"\n--- Saving clean model ---")
model.save(clean_path)
print(f"Clean model saved to: {clean_path}")

# === 5. Verify the clean model loads ===
print("\n--- Verifying clean model reloads ---")
m2 = keras.models.load_model(clean_path, compile=False)
out2 = m2.predict(dummy, verbose=0)
print(f"Verification OK! Shape={out2.shape}, argmax={out2.argmax()}")
print("\nDONE! Update brinjal_inference.py to use 'brinjal_user_clean.keras'")
