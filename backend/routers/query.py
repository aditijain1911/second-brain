from services.vector_store import search_chunks
from services.embedder import embed_text
from groq import Groq
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import traceback
import os

# Load env file manually — most reliable way
from pathlib import Path
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()

# Import groq at top level


router = APIRouter()
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
async def query_memory(request: QueryRequest):
    try:
        # 1. Embed the question
        question_embedding = embed_text([request.question])[0]

        # 2. Find relevant chunks
        results = search_chunks(question_embedding, limit=5)

        if not results:
            return {"answer": "I don't have any memories about that yet.", "sources": []}

        # 3. Build context
        context = "\n\n".join([
            f"From {r['url']}:\n{r['text']}"
            for r in results
        ])

        # 4. Ask Groq
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are the user's personal memory assistant. Answer using ONLY the provided memory snippets."
                },
                {
                    "role": "user",
                    "content": f"Memory snippets:\n\n{context}\n\nQuestion: {request.question}"
                }
            ]
        )

        return {
            "answer": response.choices[0].message.content,
            "sources": results
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "detail": traceback.format_exc()}
        )
