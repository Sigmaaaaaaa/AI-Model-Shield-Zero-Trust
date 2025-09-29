from PIL import Image
import os

# 1. Define the input path (replace with your file's name)
input_filename = 'Jpgpngtools_aerial-view-cargo-container-ship-sea-night-aerial-top-view-cargo-container-ship-sea-night-260871212_resized.webp'
output_filename = 'success_demo_224_rgb.jpg'
target_size = (224, 224)

try:
    # 2. Open the image
    img = Image.open(input_filename)
    
    # 3. CONVERT TO RGB (This is the critical step)
    # The 'convert("RGB")' operation strips the Alpha channel (A)
    if img.mode == 'RGBA':
        img = img.convert("RGB")
        print("Image successfully converted from RGBA to RGB.")
    
    # 4. Final check and resize (in case you need to resize again)
    img_resized = img.resize(target_size)
    
    # 5. Save the final file as JPEG (which is an RGB-only format)
    img_resized.save(output_filename, 'jpeg')
    print(f"Final RGB, 224x224 image saved as: {output_filename}")

except FileNotFoundError:
    print(f"ERROR: Input file '{input_filename}' not found.")
except Exception as e:
    print(f"An error occurred during conversion: {e}")