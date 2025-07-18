from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
import json
import time

from ingest import ingest_text
from rag_engine import generate_response
from utils import read_uploaded_file

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

CHAT_LOG_FILE = Path("chat_logs.json")

app.mount("/static", StaticFiles(directory="../frontend", html=True), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("../frontend/public/index.html") as f:
        return HTMLResponse(f.read())

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    question = data.get("question", "")
    response, context = await generate_response(question)

    # Log chat
    log_entry = {
        "timestamp": time.time(),
        "question": question,
        "response": response,
        "context": context,
    }

    logs = []
    if CHAT_LOG_FILE.exists():
        with CHAT_LOG_FILE.open("r") as f:
            logs = json.load(f)

    logs.append(log_entry)
    with CHAT_LOG_FILE.open("w") as f:
        json.dump(logs, f, indent=2)

    return JSONResponse({"response": response})

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    text = read_uploaded_file(file_path)
    await ingest_text(text)
    return {"status": "success", "filename": file.filename}
