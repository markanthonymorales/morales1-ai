import os
import fitz  # PyMuPDF
import markdown
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import httpx
import uuid
from pprint import pprint
from fastapi.responses import JSONResponse

# Qdrant connection
qdrant = QdrantClient(host="qdrant", port=6333)
COLLECTION_NAME = "morales1"

# Ensure collection exists
def ensure_collection():
    if COLLECTION_NAME not in [c.name for c in qdrant.get_collections().collections]:
        qdrant.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )

ensure_collection()

# Embedding via Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

async def embed_text(text: str) -> list:
    model_name = os.getenv("EMBEDDING_MODEL_NAME", "nomic-embed-text")
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            res = await client.post(f"{OLLAMA_BASE_URL}/api/embeddings", json={
                "model": model_name,
                "prompt": text
            })
            res.raise_for_status()  # Raise an exception for bad status codes
            return res.json()["embedding"]
    except httpx.HTTPStatusError as e:
        pprint(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        pprint(e)
        raise
    

# Search Qdrant
async def search_qdrant(embedding: list) -> list:
    pprint('search_qdrant')
    hits = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        limit=5,
    )
    return [hit.payload["text"] for hit in hits]

# Upsert documents to Qdrant
async def upsert_to_qdrant(texts: list[str]):
    points = [
        PointStruct(id=str(uuid.uuid4()), vector=await embed_text(t), payload={"text": t})
        for t in texts
    ]
    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)

# Parse content from files
async def extract_text(file_path, filetype):
    if filetype.endswith(".pdf") or filetype.endswith("pdf"):
        doc = fitz.open(file_path)
        return [page.get_text() for page in doc]
    elif filetype.endswith(".txt") or filetype.endswith("txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return [f.read()]
    elif filetype.endswith(".md") or filetype.endswith("md"):
        with open(file_path, "r", encoding="utf-8") as f:
            html = markdown.markdown(f.read())
            return [html]
    elif filetype.endswith(".csv") or filetype.endswith("csv"):
        with open(file_path, "r", encoding="utf-8") as f:
            return [f.read()]
    elif filetype.endswith(".xlsx") or filetype.endswith("xlsx"):
        with open(file_path, "r", encoding="utf-8") as f:
            return [f.read()]
    else:
        raise ValueError("Unsupported file format")

async def call_ollama(prompt: str):
    try:
        model_name = os.getenv("MODEL_NAME", "morales1")
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(f"{OLLAMA_BASE_URL}/api/generate", json={
                "model": "gemma3:4b-it-qat",
                "prompt": prompt,
                "stream": False
            })
            response.raise_for_status()
            json_response = response.json()
            pprint(json_response)

            if "error" in json_response:
                raise Exception(f"Ollama API Error: {json_response['error']}")

            return json_response["response"]
    except httpx.HTTPStatusError as e:
        pprint(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        raise  # Re-raise the exception to be handled by the caller
    except Exception as e:
        pprint(e)
        raise  # Re-raise the exception
    

