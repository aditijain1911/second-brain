from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import uuid
import os

# Cloud Qdrant — environment variables se URL aur key lo
QDRANT_URL = os.environ.get("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY", None)

if QDRANT_API_KEY:
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
else:
    client = QdrantClient(host="localhost", port=6333)

COLLECTION = "memories"

def init_collection():
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION not in names:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print("Created Qdrant collection: memories")

def store_chunks(chunks: list[dict], embeddings: list[list[float]]):
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "text": chunk["text"],
                "url": chunk["url"],
                "timestamp": chunk["timestamp"],
            }
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]
    client.upsert(collection_name=COLLECTION, points=points)
    print(f"Stored {len(points)} chunks in Qdrant")

def search_chunks(query_embedding: list[float], limit: int = 8) -> list[dict]:
    results = client.query_points(
        collection_name=COLLECTION,
        query=query_embedding,
        limit=limit,
        with_payload=True
    ).points
    return [
        {
            "text": r.payload["text"],
            "url": r.payload["url"],
            "timestamp": r.payload["timestamp"],
            "score": r.score
        }
        for r in results
    ]