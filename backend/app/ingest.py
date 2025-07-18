import os
import uuid
from fastapi import UploadFile
from util import extract_text, upsert_to_qdrant
from pprint import pprint

UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def ingest_file(file: UploadFile):
    extension = file.filename.split(".")[-1].lower()
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.{extension}")
    pprint(extension)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    pprint(file_path)
    texts = await extract_text(file_path, extension)
    pprint(texts)
    await upsert_to_qdrant(texts)
    return {"chunks": len(texts)}
