from huggingface_hub import HfApi
api = HfApi()
files = api.list_repo_tree(repo_id='chrisandrei/MegaPlant', repo_type='dataset')
total = 0
for f in files:
    if hasattr(f, 'size') and f.size:
        size_mb = f.size / (1024**2)
        print(f"{f.path}: {size_mb:.2f} MB")
        total += f.size
print(f"Total Size: {total / (1024**2):.2f} MB")
