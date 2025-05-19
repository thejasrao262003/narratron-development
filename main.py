import os
import time
from duckduckgo_search import DDGS
import requests
from PIL import Image
from io import BytesIO

# Function to read specific lines from
def read_queries_from_file(start_line, end_line, file_path='image_searches.txt'):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        return [line.strip() for line in lines[start_line-1:end_line] if line.strip()]

# Function to download and convert image
def download_and_convert(url, path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert('RGB')
        image.save(path, 'JPEG')
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

# Define image search and save function
def fetch_and_save_images(query, output_dir, max_images=20):
    with DDGS() as ddgs:
        results = ddgs.images(f"{query} without watermark", max_results=max_images*2)
        os.makedirs(output_dir, exist_ok=True)
        count = 0
        for result in results:
            if count >= max_images:
                break
            url = result.get("image")
            if url and download_and_convert(url, os.path.join(output_dir, f"image_{count+1}.jpg")):
                count += 1
        print(f"Saved {count} images for query: {query}")

start_line = 165
end_line = 166
queries = read_queries_from_file(start_line, end_line)
base_dir = "horror_images_restore"

for i, query in enumerate(queries):
    folder_name = f"{start_line + i:03d}_{query.replace(' ', '_')}"
    out_dir = os.path.join(base_dir, folder_name)
    fetch_and_save_images(query, out_dir)

    if (i + 1) % 3 == 0:
        print("🕒 Sleeping for 2 minutes to avoid rate limits...")
        time.sleep(90)
