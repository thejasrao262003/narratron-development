import json
import os
import shutil

# Replace this with the actual path to your local input images
LOCAL_INPUT_DIR = "/Users/tejas/PycharmProjects/shorts_automation_narratron"
OUTPUT_DIR = "horror_images_filtered"

KAGGLE_PREFIX = "/kaggle/input/horror-images-scenes-wise/"

# Load JSON
with open("image_descriptions.json") as f:
    data = json.load(f)

# Copy good images
for kaggle_full_path, value in data.items():
    relative_path = kaggle_full_path.replace(KAGGLE_PREFIX, "")
    source_path = os.path.join(LOCAL_INPUT_DIR, relative_path.lstrip("/"))
    dest_path = os.path.join(OUTPUT_DIR, relative_path.lstrip("/"))

    if value.get("image_quality") != "bad":
        if os.path.exists(source_path):
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy(source_path, dest_path)
            print(f"✅ Copied: {dest_path}")
        else:
            print(f"[!] Missing source: {source_path}")
    else:
        print(f"⛔ Skipped (bad): {relative_path}")
