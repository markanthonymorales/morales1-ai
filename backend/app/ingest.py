from util import embed_text, qdrant, COLLECTION, ensure_collection
from qdrant_client.http.models import PointStruct
import uuid

ensure_collection()

async def ingest_documents(text: str):
    chunks = text.split("\n\n")
    points = []
    for chunk in chunks:
        vec = await embed_text(chunk)
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vec,
            payload={"text": chunk}
        ))
    qdrant.upsert(collection_name=COLLECTION, points=points)
    return f"Ingested {len(points)} chunks."
