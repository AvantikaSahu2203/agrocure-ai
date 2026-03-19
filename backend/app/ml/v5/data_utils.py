import os
import pandas as pd
import numpy as np
from collections import Counter
import shutil

class AgriDataManager:
    """
    Utilities for balancing datasets and removing duplicates for AgroCure AI.
    """
    def __init__(self, data_root: str):
        self.data_root = data_root

    def analyze_imbalance(self, label_csv: str):
        df = pd.read_csv(label_csv)
        counts = Counter(df['label'])
        print("Class Distribution:")
        for label, count in counts.items():
            print(f"  {label}: {count}")
        return counts

    def balance_dataset(self, label_csv: str, output_csv: str, target_count: int = None):
        """
        Oversample minority classes and undersample majority classes.
        """
        df = pd.read_csv(label_csv)
        if target_count is None:
            target_count = df['label'].value_counts().median().astype(int)
            
        balanced_dfs = []
        for label, group in df.groupby('label'):
            if len(group) > target_count:
                balanced_dfs.append(group.sample(target_count, replace=False))
            else:
                balanced_dfs.append(group.sample(target_count, replace=True))
                
        balanced_df = pd.concat(balanced_dfs).shuffle()
        balanced_df.to_csv(output_csv, index=False)
        print(f"Balanced dataset saved to {output_csv}")

    def remove_duplicates(self, label_csv: str):
        """
        Remove duplicate image paths if any.
        """
        df = pd.read_csv(label_csv)
        initial_len = len(df)
        df = df.drop_duplicates(subset=['image_path'])
        print(f"Removed {initial_len - len(df)} duplicate entries.")
        return df

if __name__ == "__main__":
    # Example usage
    # manager = AgriDataManager("dataset/")
    # manager.analyze_imbalance("labels.csv")
    pass
