# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr
import tempfile
import shutil

app = FastAPI()

# Allow frontend to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_audio(audio_file: UploadFile = File(...)):
    recognizer = sr.Recognizer()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        shutil.copyfileobj(audio_file.file, tmp)
        tmp_path = tmp.name

    try:
        with sr.AudioFile(tmp_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return {"transcription": text}
    except sr.UnknownValueError:
        return {"transcription": "Could not understand the audio."}
    except sr.RequestError as e:
        return {"transcription": f"Speech Recognition API error: {e}"}
