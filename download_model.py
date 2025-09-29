# download_model.py

import tensorflow as tf
import os
import sys

# --- Configuration ---
# Set the desired filename
MODEL_FILENAME = 'original_model.h5' 
# Choose weights: 'imagenet' is standard pre-training.
# include_top=True means you get the full model ready for 1000-class classification.
# This makes it easy to use SHAP later.
MODEL_WEIGHTS = 'imagenet'

print(f"Starting download and save of MobileNetV2 with {MODEL_WEIGHTS} weights...")

try:
    # 1. Instantiate the MobileNetV2 model. 
    # The Keras Applications module automatically downloads the weights 
    # to your Keras cache folder during this step.
    model = tf.keras.applications.MobileNetV2(
        weights=MODEL_WEIGHTS,
        include_top=True,
        input_shape=(224, 224, 3) # Standard input size for MobileNetV2
    )

    # 2. Save the ENTIRE model (architecture + weights) into a single H5 file
    model.save(MODEL_FILENAME)
    
    # 3. Success Confirmation
    print("\n----------------------------------------------------")
    print(f"SUCCESS: Model saved as '{MODEL_FILENAME}' in the root directory.")
    print("Next: Run your encryption script to protect this file.")
    print("----------------------------------------------------")

except Exception as e:
    print(f"\nERROR: Model download or save failed.")
    print(f"Details: {e}")
    sys.exit(1)

# Clean up the acquisition script (optional but good practice)
# os.remove(__file__)