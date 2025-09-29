# src/validator.py

import io
from PIL import Image

# Define the expected properties for a clean satellite image input
# MobileNetV2 requires a 224x224x3 input shape
EXPECTED_WIDTH, EXPECTED_HEIGHT = 224, 224
MIN_FILE_SIZE_KB = 1  # Arbitrary lower bound to detect empty/malicious tiny files
MAX_FILE_SIZE_KB = 5000 # Arbitrary upper bound to prevent DoS attacks


def validate_image_integrity(image_bytes: bytes) -> tuple[bool, str]:
    """
    Checks the integrity and shape of the image against expected norms.
    Returns (is_valid, reason)
    """
    file_size_kb = len(image_bytes) / 1024

    # 1. File Size Check (Prevent Denial-of-Service/Tiny Corruption)
    if file_size_kb < MIN_FILE_SIZE_KB or file_size_kb > MAX_FILE_SIZE_KB:
        return False, "Input failed file size check (Poisoning/DoS Risk)."

    try:
        # 2. Image Decoding Check (Prevent Malformed Payloads)
        img = Image.open(io.BytesIO(image_bytes))
    except Exception:
        return False, "Input failed image decoding check (Malformed Payload)."

    # 3. Image Dimensions Check (Ensure compatibility for the model)
    if img.size != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        return False, f"Input failed dimension check. Expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}, got {img.size}."
    
    # 4. Color Channels Check (Ensure RGB)
    if img.mode != 'RGB':
        return False, f"Input failed color channel check. Expected RGB, got {img.mode}."

    return True, "Data integrity passed."