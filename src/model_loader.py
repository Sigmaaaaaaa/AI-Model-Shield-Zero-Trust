# src/model_loader.py

import os
import io
import hashlib
import sys
import tensorflow as tf
from dotenv import load_dotenv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Load the environment variables
load_dotenv()
ENCRYPTION_KEY_STR = os.getenv("MODEL_ENCRYPTION_KEY")
ENCRYPTED_MODEL_PATH = 'models/encrypted_model.bin'


def decrypt_file_to_bytes(key: bytes, filepath: str) -> bytes | None:
    """Reads encrypted file, decrypts it, and returns the plaintext model bytes."""
    try:
        if not os.path.exists(filepath):
            print(f"ERROR: Encrypted model not found at {filepath}")
            return None

        # 1. Read the file
        with open(filepath, 'rb') as f:
            data = f.read()

        # 2. Extract IV (first 16 bytes) and Ciphertext
        iv = data[:16]
        ciphertext = data[16:]
        
        # Ensure key is 32 bytes (256 bits) for AES-256
        if len(key) != 32:
            key = hashlib.sha256(key).digest() 

        # 3. Setup the Decryptor
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # 4. Decrypt and Return
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext

    except Exception as e:
        print(f"DECRYPTION FAILED: {e}")
        return None

def load_secure_model():
    """Decrypts the model IP and loads it into Keras in memory."""
    try:
        key_bytes = ENCRYPTION_KEY_STR.encode()
        
        # 1. Decrypt the model bytes
        model_bytes = decrypt_file_to_bytes(key_bytes, ENCRYPTED_MODEL_PATH)
        if model_bytes is None:
            sys.exit(1)

        # 2. Load the Keras model from the decrypted bytes in memory
        # We use io.BytesIO and load_model, which expects a path-like object 
        # but can handle file content via the BytesIO object.
        model_file = io.BytesIO(model_bytes)
        
        # TensorFlow 2.x requires the model to be saved temporarily to disk to load 
        # from the HDF5 format, which is not ideal for 'in-memory' security.
        # HACKATHON SOLUTION: Temporarily save to a secure /tmp folder path 
        # and delete immediately after loading to maintain integrity.
        
        temp_path = '/tmp/temp_model.h5' if os.name != 'nt' else 'temp_model_ip.h5'
        with open(temp_path, 'wb') as f:
            f.write(model_bytes)
        
        model = tf.keras.models.load_model(temp_path)
        os.remove(temp_path) # Delete the temporary file immediately

        print("Model decryption successful. Model loaded in memory.")
        return model
    
    except Exception as e:
        print(f"MODEL LOADING FAILED: {e}")
        return None