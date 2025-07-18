from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import os

from ingest import ingest_file
from rag_engine import generate_response
from pprint import pprint

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dynamically calculate path
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "../frontend")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open(static_dir +"/public/index.html") as f:
        return HTMLResponse(f.read())

@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    question = data.get("message", "")
    try:
        pprint(question)
        answer = await generate_response(question)
        return JSONResponse(content={"answer": answer})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        result = await ingest_file(file)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
