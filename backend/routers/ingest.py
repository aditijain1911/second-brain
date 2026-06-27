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
    # Save raw document metadata
    save_document(payload)

    # Split text into chunks
    chunks = chunk_text(
        payload.text,
        payload.url,
        payload.timestamp.isoformat()
    )

    # Generate embeddings
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_text(texts)

    # Attach embeddings to each chunk
    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding

    # Store in Qdrant
    await store_chunks(chunks)