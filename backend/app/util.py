import httpx
from pathlib import Path
import fitz  # PyMuPDF
import markdown
import os

async def embed_text(text: str):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://ollama:11434/api/embeddings", json={
            "model": "morales1",
            "prompt": text
        })
        return response.json()["embedding"]

async def search_qdrant(vector):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://qdrant:6333/collections/morales1/points/search", json={
            "vector": vector,
            "top": 5,
            "with_payload": True
        })
        return [item["payload"]["text"] for item in response.json().get("result", [])]

async def call_ollama(prompt: str):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://ollama:11434/api/generate", json={
            "model": "morales1",
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"]

def read_uploaded_file(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        doc = fitz.open(path)
        return "\n".join(page.get_text() for page in doc)
    elif ext in [".txt", ".md"]:
        with path.open("r", encoding="utf-8") as f:
            content = f.read()
        if ext == ".md":
            return markdown.markdown(content)
        return content
    else:
        raise ValueError("Unsupported file type")
