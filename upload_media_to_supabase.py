"""
One-off script to upload local Django MEDIA_ROOT files to Supabase Storage
(S3-compatible endpoint), preserving folder structure.

Usage:
    python upload_media_to_supabase.py

Requires: boto3 (pip install boto3 --break-system-packages if needed)
Reads credentials from your existing .env via python-decouple, so no
secrets need to be hardcoded here.
"""

import os
from decouple import config
import boto3
from botocore.exceptions import ClientError

# --- Config (pulled from your .env, same values Django uses) ---
ENDPOINT_URL = config('SUPABASE_S3_ENDPOINT')          # e.g. https://<ref>.storage.supabase.co/storage/v1/s3
ACCESS_KEY = config('SUPABASE_S3_ACCESS_KEY')
SECRET_KEY = config('SUPABASE_S3_SECRET_KEY')
BUCKET = config('SUPABASE_S3_BUCKET', default='media')
REGION = config('SUPABASE_S3_REGION', default='us-east-1')

# Local media folder (adjust if your MEDIA_ROOT differs)
LOCAL_MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')

def main():
    if not os.path.isdir(LOCAL_MEDIA_DIR):
        print(f"ERROR: local media folder not found at: {LOCAL_MEDIA_DIR}")
        print("Edit LOCAL_MEDIA_DIR in this script to point at your actual MEDIA_ROOT.")
        return

    s3 = boto3.client(
        "s3",
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION,
    )

    uploaded, skipped, failed = 0, 0, 0

    for root, dirs, files in os.walk(LOCAL_MEDIA_DIR):
        for filename in files:
            local_path = os.path.join(root, filename)
            relative_path = os.path.relpath(local_path, LOCAL_MEDIA_DIR).replace("\\", "/")

            try:
                s3.upload_file(local_path, BUCKET, relative_path)
                print(f"Uploaded: {relative_path}")
                uploaded += 1
            except ClientError as e:
                print(f"FAILED: {relative_path} -> {e}")
                failed += 1

    print(f"\nDone. Uploaded: {uploaded}, Failed: {failed}")

if __name__ == "__main__":
    main()