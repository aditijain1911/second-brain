from sentence_transformers import SentenceTransformer

# This downloads a ~80MB model the first time — wait for it
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(texts: list[str]) -> list[list[float]]:
    embeddings = model.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()