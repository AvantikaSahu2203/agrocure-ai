import os
import shutil
import hashlib
import pandas as pd
from tqdm import tqdm
from PIL import Image
from app.ml.v6.utils.phash_utils import compute_phash, compare_hashes

class AgriDataIntegrator:
    """
    AgroCure AI Data Integrator
    Handles merging, deduplication, and normalization of PlantVillage and Multi-Crop datasets.
    """
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.image_hashes = set()
        self.metadata = []
        
        # Ensure output structure
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)

    def get_file_hash(self, filepath: str) -> str:
        """Generate SHA-256 hash for exact deduplication."""
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def get_perceptual_hash(self, filepath: str) -> str:
        """Wrapper for 64-bit pHash."""
        try:
            return compute_phash(filepath)
        except Exception:
            return "0" * 16

    def is_duplicate(self, new_hash: str, cutoff: int = 8) -> bool:
        """Check if hash is already present within Hamming distance cutoff."""
        for existing_hash in self.image_hashes:
            if compare_hashes(new_hash, existing_hash) < cutoff:
                return True
        return False

    def normalize_label(self, raw_label: str) -> str:
        """
        Normalize class names across datasets.
        Example: 'Tomato___Leaf_Mold' -> 'Tomato__Leaf_Mold'
        """
        # Specific mappings to handle inconsistent folder names in PlantVillage
        mapping = {
            "Pepper__bell___Bacterial_spot": "Pepper__Bacterial_Spot",
            "Pepper__bell___healthy": "Pepper__Healthy",
            "Potato___Early_blight": "Potato__Early_Blight",
            "Potato___Late_blight": "Potato__Late_Blight",
            "Potato___healthy": "Potato__Healthy",
            "Tomato_Bacterial_spot": "Tomato__Bacterial_Spot",
            "Tomato_Early_blight": "Tomato__Early_Blight",
            "Tomato_Late_blight": "Tomato__Late_Blight",
            "Tomato_Leaf_Mold": "Tomato__Leaf_Mold",
            "Tomato_Septoria_leaf_spot": "Tomato__Leaf_Spot",
            "Tomato_Spider_mites_Two_spotted_spider_mite": "Tomato__Mite_Damage",
            "Tomato__Target_Spot": "Tomato__Fungal_Spot",
            "Tomato__Tomato_YellowLeaf__Curl_Virus": "Tomato__Viral_Mosaic",
            "Tomato__Tomato_mosaic_virus": "Tomato__Viral_Mosaic",
            "Tomato_healthy": "Tomato__Healthy",
        }
        
        normalized = mapping.get(raw_label)
        if normalized:
            return normalized
            
        # Fallback normalization
        label = raw_label.replace('___', '__').replace(' ', '_')
        return label

    def integrate_dataset(self, dataset_path: str, dataset_name: str):
        """
        Walk through a dataset directory and integrate images.
        Expected structure: dataset_path/class_folder/image.jpg
        """
        print(f"Integrating {dataset_name} from {dataset_path}...")
        
        for class_folder in tqdm(os.listdir(dataset_path)):
            class_path = os.path.join(dataset_path, class_folder)
            if not os.path.isdir(class_path):
                continue
            
            normalized_class = self.normalize_label(class_folder)
            
            for img_name in os.listdir(class_path):
                img_path = os.path.join(class_path, img_name)
                if not img_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue
                
                # pHash-based near-duplicate detection
                img_phash = self.get_perceptual_hash(img_path)
                if self.is_duplicate(img_phash, cutoff=8):
                    continue
                self.image_hashes.add(img_phash)
                
                # SHA256 for exact match secondary guard
                img_sha = self.get_file_hash(img_path)
                
                # Generate unique filename
                ext = os.path.splitext(img_name)[1]
                new_filename = f"{dataset_name}_{img_sha[:16]}{ext}"
                dest_path = os.path.join(self.output_dir, "images", new_filename)
                
                # Copy file
                shutil.copy2(img_path, dest_path)
                
                # Append metadata
                self.metadata.append({
                    "image_path": os.path.join("images", new_filename),
                    "raw_label": class_folder,
                    "normalized_label": normalized_class,
                    "dataset": dataset_name,
                    "sha256": img_sha,
                    "phash": img_phash
                })

    def get_balanced_metadata(self, max_healthy_ratio: float = 0.4) -> List[Dict]:
        """
        Return a balanced version of the metadata.
        Ensures 'Healthy' classes combined do not exceed the specified ratio.
        """
        df = pd.DataFrame(self.metadata)
        if df.empty:
            return []

        # Identify healthy samples (case-insensitive match for 'healthy')
        healthy_mask = df['normalized_label'].str.contains('healthy', case=False, na=False)
        healthy_df = df[healthy_mask]
        diseased_df = df[~healthy_mask]

        num_diseased = len(diseased_df)
        if num_diseased == 0:
            return self.metadata

        # Max healthy allowed = (num_diseased / (1 - ratio)) * ratio
        max_healthy = int((max_healthy_ratio / (1 - max_healthy_ratio)) * num_diseased)

        if len(healthy_df) > max_healthy:
            print(f"Balancing: Downsampling Healthy from {len(healthy_df)} to {max_healthy}")
            healthy_df = healthy_df.sample(n=max_healthy, random_state=42)
        
        balanced_df = pd.concat([diseased_df, healthy_df])
        return balanced_df.to_dict('records')

    def save_metadata(self, filename: str = "unified_metadata.csv", balanced: bool = True):
        """Save the unified metadata to a CSV file."""
        if balanced:
            data_to_save = self.get_balanced_metadata()
        else:
            data_to_save = self.metadata
            
        df = pd.DataFrame(data_to_save)
        output_path = os.path.join(self.output_dir, filename)
        df.to_csv(output_path, index=False)
        
        print(f"Unified metadata saved to {output_path}")
        print(f"Total unique images: {len(df)}")
        print(f"Total unique classes: {df['normalized_label'].nunique()}")

if __name__ == "__main__":
    # Example usage (paths would be provided by user or environment)
    # integrator = AgriDataIntegrator("dataset_unified")
    # integrator.integrate_dataset("path/to/PlantVillage", "PlantVillage")
    # integrator.integrate_dataset("path/to/MultiCrop", "MultiCrop")
    # integrator.save_metadata()
    pass
