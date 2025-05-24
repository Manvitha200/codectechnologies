from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        text = "Could not understand audio"
    except sr.RequestError:
        text = "Speech recognition service unavailable"

    return {"transcription": text}
