from io import BytesIO

import boto3
from dotenv import load_dotenv
import os
from PIL import Image
from botocore.client import Config

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
BUCKET_NAME = "narratron"
upload_directory = "images"

s3_client = boto3.client(
    "s3",
    region_name='us-east-1',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# base_dir = "horror_images_final/"
# sub_dir = "horror_images_restore/"
#
# for full_path in os.listdir(base_dir+sub_dir):
#     real_path = full_path
#     cleaned = real_path.split("_", 1)[1]
#     for image in os.listdir(base_dir+sub_dir+real_path):
#         image_path = os.path.join(base_dir+sub_dir+real_path, image)
#         image_new = Image.open(image_path)
#         rgb_image = image_new.convert('RGB')
#         byte_io = BytesIO()
#         rgb_image.save(byte_io, 'JPEG')
#         byte_io.seek(0)
#         file_path = f"{upload_directory}/{cleaned}/{image}"
#         print(f"Uploading {file_path}...")
#         s3_client.upload_fileobj(byte_io, BUCKET_NAME, file_path,
#                                  ExtraArgs={'ContentType': 'image/jpeg'})
#         print("Uploaded Successfully\n")
#         presigned_url = s3_client.generate_presigned_url(
#             'get_object',
#             Params={'Bucket': BUCKET_NAME, 'Key': file_path},
#             ExpiresIn= 7 * 24 * 60 * 60
#         )
#         print(f"Presigned URL: {presigned_url}")