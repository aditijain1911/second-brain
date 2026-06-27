from services.embedder import model as embed_model
from services.vector_store import client, COLLECTION
from qdrant_client.models import Filter, FieldCondition, Range
from anthropic import Anthropic
from datetime import datetime, timedelta

llm = Anthropic()

def parse_time_filter(query: str) -> dict | None:
    """Extract time intent from natural language."""
    now = datetime.utcnow()
    
    time_map = {
        "today": now - timedelta(days=1),
        "yesterday": now - timedelta(days=2),
        "last week": now - timedelta(weeks=1),
        "this week": now - timedelta(days=7),
        "last month": now - timedelta(days=30),
    }
    
    query_lower = query.lower()
    for phrase, cutoff in time_map.items():
        if phrase in query_lower:
            return {"gte": cutoff.timestamp()}
    return None

async def query_memory(question: str, top_k: int = 8) -> dict:
    # 1. Embed the question
    q_embedding = embed_model.encode([question], normalize_embeddings=True)[0].tolist()
    
    # 2. Build time filter if needed
    time_range = parse_time_filter(question)
    qdrant_filter = None
    if time_range:
        qdrant_filter = Filter(
            must=[FieldCondition(
                key="timestamp",
                range=Range(**time_range)
            )]
        )
    
    # 3. Semantic search
    results = client.search(
        collection_name=COLLECTION,
        query_vector=q_embedding,
        query_filter=qdrant_filter,
        limit=top_k,
        with_payload=True
    )
    
    if not results:
        return {"answer": "I don't have any memories about that yet.", "sources": []}
    
    # 4. Build context for LLM
    context_parts = []
    sources = []
    for r in results:
        p = r.payload
        context_parts.append(f"[Source: {p['url']} | {p['timestamp']}]\n{p['text']}")
        sources.append({"url": p["url"], "title": p.get("title", p["url"]), 
                        "timestamp": p["timestamp"], "score": r.score})
    
    context = "\n\n---\n\n".join(context_parts)
    
    # 5. LLM answer with streaming
    system = """You are the user's personal memory assistant. 
Answer questions using ONLY the provided memory snippets.
Always cite which source you're drawing from.
If the memory is incomplete, say so honestly."""
    
    response = llm.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system,
        messages=[{
            "role": "user",
            "content": f"Memory snippets:\n\n{context}\n\nQuestion: {question}"
        }]
    )
    
    return {
        "answer": response.content[0].text,
        "sources": sources[:5]
    }