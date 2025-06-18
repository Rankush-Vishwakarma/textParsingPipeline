# app/pipeline.py
import json
from utils import storage
import io
from extractor import extract_text
from config import GCS_BUCKET, GCS_OUTPUT_FOLDER

def run_pipeline(input_path, output_path):
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET)
    blob = bucket.blob(input_path)
    content = blob.download_as_bytes()
    extracted_text = extract_text(content, input_path)
    output_blob = bucket.blob(output_path)
    output_blob.upload_from_string(json.dumps({"text": extracted_text}))
    return extracted_text

