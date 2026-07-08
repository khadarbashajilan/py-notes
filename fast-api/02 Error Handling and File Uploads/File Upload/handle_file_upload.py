from fastapi import FastAPI, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
import filetype
import uuid
import os

app = FastAPI()
UPLOAD_DIR="public_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name='static')

async def process_upload(request, file):
    contents = await file.read()
    kind = filetype.guess(contents)

    if not kind or not kind.mime in ["image/jpeg", "image/png"]:
        return {"error" : "Invalid image type"}

    size_in_bytes = len(contents)

    if size_in_bytes > 1024*1024*2:
        return {"error" : "Size of the file should not exceed 2MB"}


    safe_filename = f"{uuid.uuid4()}.{kind.extension}"

    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(file_path, "wb") as f:
        f.write(contents)

    base_url = str(request.base_url)

    file_url=f"{base_url}static/{safe_filename}"

    return {
            "message": "File Uploaded Successfully!",
            "filename":safe_filename,
            "file_url":file_url
            }

@app.post('/upload-pic')
async def upload_file(request:Request, file:UploadFile = File(...)):
    return await process_upload(request, file)


