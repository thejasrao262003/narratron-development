from content_creation import *
from mongo_connection import insert_story_document, update_bg_music, get_scenes, push_image_file_names
from s3_operations import get_files, generate_presigned_url, upload_audio_file
from voice_generation import generate_audio
from combine_audio_image import create_video
import random

# Generate story
response = generate_script()
# Convert string to JSON
json_response = extract_json_from_markdown(response)
# Insert into MongoDB
insert_story_document(json_response)
#Get all bg_musics
file_keys = get_files("narratron", "bg_musics/")
#Filter only audio files
bg_musics = [key for key in file_keys if key.endswith(".mp3") or key.endswith(".wav")]
# Select on in random
num = random.randint(0, len(bg_musics)-1)
update_bg_music(bg_musics[num])

# Get each scene for the story
scenes = get_scenes()

# generating audio and sending it to S3 for storage
audio_file_names = generate_audio(scenes)

# mapping images to scenes
image_file_names = []
for key, value in scenes.items():
    file_name = f'images/{value["scene_name"].replace(" ", "_").lower()}'
    image_file_keys = get_files("narratron", file_name)
    num = random.randint(0, len(image_file_keys)-1)
    image_file_names.append(image_file_keys[num])

push_image_file_names(image_file_names)
img_presigned_urls = []
for image in image_file_names:
    presigned_url = generate_presigned_url(image)
    img_presigned_urls.append(presigned_url)

bg_music_presigned_url = generate_presigned_url(bg_musics[num])

audio_presigned_urls = []
for audio in audio_file_names:
    presigned_url = generate_presigned_url(audio)
    audio_presigned_urls.append(presigned_url)

create_video(img_presigned_urls, audio_presigned_urls, bg_music_presigned_url)
with open("/tmp/FinalShorts/combined_shorts.mp4", "rb") as f:
    upload_audio_file(f, "final_outputs/video_output.mp4", "narratron")

