import uuid, os, json
from google.cloud import storage
from config import GCS_BUCKET, GCS_INPUT_FOLDER
from hashingMap import compute_file_hash
import io
def upload_to_gcs(file=None, url=None):
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET)
    filename = str(uuid.uuid4())
    if file:
        content = file.file.read()
        ext = os.path.splitext(file.filename)[1].lower().lstrip('.')
        content_hash = compute_file_hash(content)
        blob_name = f"{GCS_INPUT_FOLDER}/{content_hash}.{ext}"
        blob = bucket.blob(blob_name)
        if blob.exists():
            return blob_name, f"output/{content_hash}.json"
        blob.upload_from_string(content)
        return blob_name, f"output/{content_hash}.json"
    elif url:
        import requests
        content = requests.get(url).text.encode('utf-8')
        ext = 'html'
        content_hash = compute_file_hash(content)
        blob_name = f"{GCS_INPUT_FOLDER}/{content_hash}.{ext}"
        blob = bucket.blob(blob_name)
        if not blob.exists():
            blob.upload_from_string(content)
        return blob_name, f"output/{content_hash}.json"
