# This script is a simpler alternative to onnx2tf for Python 3.10.0
import os

print("--- Step 1: Installing required tools ---")
# Removed s_tflite (typo) and using compatible versions
os.system("pip install onnx onnx2tf==1.17.5 onnx_graphsurgeon")

print("\n--- Step 2: Attempting Conversion ---")
# Running the converter with some "safe" flags for mobile
os.system("onnx2tf -i crop_model_v7.onnx -o crop_model_v7.tflite")

if os.path.exists("crop_model_v7.tflite"):
    print("\n[SUCCESS] crop_model_v7.tflite created!")
else:
    print("\n[FAILED] TFLite file was not created. Attempting fallback...")
    # Fallback to a different command if onnx2tf fails
    os.system("onnx2tf -i crop_model_v7.onnx -o crop_model_v7.tflite --non_verbose")
