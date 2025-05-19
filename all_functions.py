import boto3
from dotenv import load_dotenv
import os

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
BUCKET_NAME = "narratron"

s3_client = boto3.client(
    "s3",
    region_name='us-east-1',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def get_files(bucket_name, directory):
    try:
        if not directory.endswith("/"):
            directory += "/"
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=directory)
        files = []
        if 'Contents' in response:
            for file in response['Contents']:
                files.append(file['Key'])
        return files
    except Exception as e:
        print(f"Error: {e}")
        return []

# Example usage
file_keys = get_files(BUCKET_NAME, "bg_musics")
for key in file_keys:
    print("📂", key)
