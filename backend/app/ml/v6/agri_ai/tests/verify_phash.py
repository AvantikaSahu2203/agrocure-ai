import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.phash_utils import compute_phash, compare_hashes
from PIL import Image, ImageEnhance
import numpy as np

def test_phash_robustness():
    """
    Test pHash behavior under common image variations.
    """
    print("Testing pHash Robustness...")
    
    # Create white image with some random dots for texture
    img_data = np.ones((512, 512, 3), dtype=np.uint8) * 255
    cv2.circle(img_data, (256, 256), 50, (0, 0, 0), -1)
    original_img = Image.fromarray(img_data)
    original_img.save("test_orig.jpg")
    
    hash_orig = compute_phash("test_orig.jpg")
    print(f"Original Hash: {hash_orig}")
    
    # 1. Test Brightness Change
    bright_img = ImageEnhance.Brightness(original_img).enhance(1.5)
    bright_img.save("test_bright.jpg")
    hash_bright = compute_phash("test_bright.jpg")
    dist_bright = compare_hashes(hash_orig, hash_bright)
    print(f"Brightness Shift Distance: {dist_bright} (Should be < 4)")
    
    # 2. Test Small Rotation
    rot_img = original_img.rotate(5)
    rot_img.save("test_rot.jpg")
    hash_rot = compute_phash("test_rot.jpg")
    dist_rot = compare_hashes(hash_orig, hash_rot)
    print(f"5-degree Rotation Distance: {dist_rot} (Should be < 8)")
    
    # 3. Test Compression Artifacts
    original_img.save("test_low_q.jpg", quality=10)
    hash_low_q = compute_phash("test_low_q.jpg")
    dist_low_q = compare_hashes(hash_orig, hash_low_q)
    print(f"Low Quality Distance: {dist_low_q} (Should be < 4)")

    # Clean up
    for f in ["test_orig.jpg", "test_bright.jpg", "test_rot.jpg", "test_low_q.jpg"]:
        if os.path.exists(f): os.remove(f)

if __name__ == "__main__":
    import cv2
    test_phash_robustness()
