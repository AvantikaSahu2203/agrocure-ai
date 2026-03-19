import numpy as np
import cv2
from PIL import Image
from typing import Union

def compute_phash(image: Union[str, Image.Image]) -> str:
    """
    Generate a 64-bit Perceptual Hash (pHash) for an image.
    Uses DCT (Discrete Cosine Transform) for frequency-based hashing.
    """
    if isinstance(image, str):
        image = Image.open(image).convert('L')
    else:
        image = image.convert('L')
        
    # Resize to 32x32
    image = image.resize((32, 32), Image.Resampling.LANCZOS)
    pixels = np.array(image, dtype=np.float32)
    
    # Compute 2D DCT
    dct = cv2.dct(pixels)
    
    # Extract top-left 8x8 (excluding DC component at [0,0] if preferred, but usually we keep it)
    dct_low = dct[:8, :8]
    
    # Calculate median (robust to lighting)
    median = np.median(dct_low)
    
    # Generate 64-bit string
    diff = dct_low > median
    bits = "".join(['1' if b else '0' for b in diff.flatten()])
    
    # Convert to 16-char hex
    return hex(int(bits, 2))[2:].zfill(16)

def compare_hashes(hash1: str, hash2: str) -> int:
    """
    Calculate Hamming distance between two hex hashes.
    Distance < 8  => Near duplicate (Remove)
    Distance 8-12 => Possible duplicate (Flag)
    """
    # Convert hex to integer
    h1 = int(hash1, 16)
    h2 = int(hash2, 16)
    
    # XOR and count set bits (bin() is easy in Python)
    return bin(h1 ^ h2).count('1')

if __name__ == "__main__":
    # Quick test
    h1 = "f0f0f0f0f0f0f0f0"
    h2 = "f0f0f0f0f0f0f0f1" # 1 bit difference
    print(f"Distance: {compare_hashes(h1, h2)}")
