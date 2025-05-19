# from PIL import Image
# import os
#
# input_dir = "horror_images_filtered/horror_images_restore"
# output_dir = "horror_images_filtered/horror_images_shorts"
# os.makedirs(output_dir, exist_ok=True)
#
# TARGET_ASPECT_RATIO = 9 / 16
# TARGET_SIZE = (1080, 1920)
#
# def center_crop_to_aspect(img, target_ratio):
#     width, height = img.size
#     current_ratio = width / height
#
#     if current_ratio > target_ratio:
#         # Too wide – crop width
#         new_width = int(height * target_ratio)
#         offset = (width - new_width) // 2
#         return img.crop((offset, 0, offset + new_width, height))
#     else:
#         # Too tall – crop height
#         new_height = int(width / target_ratio)
#         offset = (height - new_height) // 2
#         return img.crop((0, offset, width, offset + new_height))
#
# for subfolder in os.listdir(input_dir):
#     sub_path = os.path.join(input_dir, subfolder)
#     if not os.path.isdir(sub_path):
#         continue
#
#     out_subfolder = os.path.join(output_dir, subfolder)
#     os.makedirs(out_subfolder, exist_ok=True)
#
#     for img_name in os.listdir(sub_path):
#         img_path = os.path.join(sub_path, img_name)
#         try:
#             with Image.open(img_path) as img:
#                 cropped = center_crop_to_aspect(img, TARGET_ASPECT_RATIO)
#                 resized = cropped.resize(TARGET_SIZE, Image.LANCZOS)
#                 out_path = os.path.join(out_subfolder, img_name)
#                 resized.save(out_path)
#                 print(f"✅ Saved {out_path}")
#         except Exception as e:
#             print(f"❌ Failed {img_path}: {e}")
import json
import os
import shutil

new_image_path = "horror_images_final"

with open("image_descriptions.json") as f:
    data = json.load(f)

    for full_path, value in data.items():
        if value.get("image_quality") != "bad" and value.get("image_relevance", 0) >= 8:
            # Preserve folder structure
            dest_path = os.path.join(new_image_path, full_path)
            dest_folder = os.path.dirname(dest_path)

            # Ensure destination directory exists
            os.makedirs(dest_folder, exist_ok=True)

            # Copy file if it exists
            if os.path.exists(full_path):
                shutil.copy2(full_path, dest_path)
            else:
                print(f"❌ Image not found: {full_path}")

