import mimetypes
import tempfile
import os
import requests
from fastapi import FastAPI, File, UploadFile, HTTPException
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()
app = FastAPI()

BLOB_TOKEN = os.getenv("BLOB_READ_WRITE_TOKEN")
STORE_ID   = os.getenv("STORE_ID")
API_URL    = "https://blob.vercel-storage.com/api/blob/upload"

@app.post("/uploads")
async def upload_to_blob(file: UploadFile = File(...)):
    if not BLOB_TOKEN or not STORE_ID:
        raise HTTPException(500, "Missing Vercel Blob credentials")

    # Determine folder
    ext = os.path.splitext(file.filename)[1].lower()
    folder = "images" if ext in (".jpg",".jpeg",".png") else "videos"
    filename = f"{folder}/{uuid4().hex}{ext}"

    # Write to a temp file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # Build multipart form-data
        files = {
            "file": (filename, open(tmp_path, "rb"), mimetypes.guess_type(file.filename)[0] or "application/octet-stream")
        }
        # POST with storeId query
        resp = requests.post(
            f"{API_URL}?storeId={STORE_ID}",
            headers={"Authorization": f"Bearer {BLOB_TOKEN}"},
            files=files
        )

        if resp.status_code != 200:
            raise HTTPException(500, f"Upload failed ({resp.status_code}): {resp.text}")

        data = resp.json()
        return {"url": data["url"]}

    finally:
        os.remove(tmp_path)
