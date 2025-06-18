from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from utils import upload_to_gcs
from pipeline import run_pipeline
import io
from typing import List
from concurrent.futures import ThreadPoolExecutor


app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        input_path, output_path = upload_to_gcs(file=file)
        result = run_pipeline(input_path, output_path)
        return {"output_path": output_path, "sample": result[:200]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-url/")
async def upload_url(url: str = Form(...)):
    try:
        input_path, output_path = upload_to_gcs(url=url)
        result = run_pipeline(input_path, output_path)
        return {"output_path": output_path, "sample": result[:200]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

'''Handling the multiple files to process simultenously'''
@app.post("/upload-multiple/")
async def upload_multiple(files: List[UploadFile] = File(...)):
    results = []

    def process_file(file):
        input_path, output_path = upload_to_gcs(file=file)
        result = run_pipeline(input_path, output_path)
        return {
            "filename": file.filename,
            "output_path": output_path,
            "sample": result[:200]
        }

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_file, f) for f in files]
        for future in futures:
            try:
                results.append(future.result())
            except Exception as e:
                results.append({"error": str(e)})

    return {"files": results}


