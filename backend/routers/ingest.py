from fastapi import APIRouter, BackgroundTasks
from models.schemas import IngestPayload
from db.metadata import save_document
from services.chunker import chunk_text
from services.embedder import embed_text
from services.vector_store import store_chunks

router = APIRouter()


@router.post("/ingest")
async def ingest(payload: IngestPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(process, payload)
    return {
        "status": "queued",
        "title": payload.title
    }


async def process(payload: IngestPayload):
    # Try saving to SQLite, but don't crash if it fails
    try:
        save_document(payload)
    except Exception as e:
        print(f"SQLite save failed (non-critical): {e}")

    chunks = chunk_text(
        payload.text,
        payload.url,
        payload.timestamp.isoformat()
    )

    if not chunks:
        return

    texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_text(texts)

    store_chunks(chunks, embeddings)