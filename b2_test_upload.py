import boto3

# Backblaze S3 settings
ENDPOINT = "https://s3.us-east-005.backblazeb2.com"
BUCKET_NAME = "etl-data-lake"

# ⚠️ IMPORTANT: replace these with your actual keys
ACCESS_KEY_ID = "0054f37cdc048cf0000000001"
SECRET_ACCESS_KEY = "K005Zw7ngwVDogmNv7dc7houdqmM1K8"

# Create S3 client
s3 = boto3.client(
    "s3",
    endpoint_url=ENDPOINT,
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY
)

print("Connection created successfully")

s3.upload_file(
    Filename="test_upload.txt",
    Bucket="etl-data-lake",
    Key="bronze/test_upload.txt"
)

print("Uploaded successfully")