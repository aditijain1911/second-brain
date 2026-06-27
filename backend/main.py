from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.ingest import router as ingest_router
from routers.query import router as query_router
from db.metadata import create_db
from services.vector_store import init_collection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

create_db()
init_collection()

app.include_router(ingest_router)
app.include_router(query_router)


@app.get("/")
def home():
    return {"message": "Second Brain backend is alive!"}


@app.get("/memories")
def get_memories():
    from db.metadata import engine, Document
    from sqlmodel import Session, select
    with Session(engine) as session:
        docs = session.exec(select(Document)).all()
        return [{"url": d.url, "title": d.title, "timestamp": str(d.timestamp)} for d in docs]


@app.post("/reindex")
def reindex():
    from db.metadata import engine, Document
    from sqlmodel import Session, select
    from services.chunker import chunk_text
    from services.embedder import embed_text
    from services.vector_store import store_chunks
    with Session(engine) as session:
        docs = session.exec(select(Document)).all()
        count = 0
        for doc in docs:
            chunks = chunk_text(doc.text, doc.url, doc.timestamp.isoformat())
            if chunks:
                texts = [c["text"] for c in chunks]
                embeddings = embed_text(texts)
                store_chunks(chunks, embeddings)
                count += 1
        return {"reindexed": count}
