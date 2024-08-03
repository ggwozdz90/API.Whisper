"""
api.py
---

The REST Api.
"""

import os
from datetime import datetime

import whisper
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

UPLOAD_DIR = os.path.join(os.getcwd(), "uploadedFiles")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def welcome():
    date = datetime.now()
    return {"message": f"Welcome to the API at {date}"}


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    model = whisper.load_model("base")
    result = model.transcribe(file_location, fp16=False)

    return JSONResponse(
        content={
            "filename": file.filename,
            "content_type": file.content_type,
            "location": file_location,
            "transcription": result["text"],
        }
    )
