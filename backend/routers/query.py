from services.vector_store import search_chunks
from services.embedder import embed_text
from groq import Groq
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import traceback
import os

router = APIRouter()

GROQ_KEY = os.environ.get("GROQ_API_KEY")
print(f"DEBUG: GROQ_API_KEY found = {GROQ_KEY is not None}")
if GROQ_KEY:
    print(f"DEBUG: Key starts with = {GROQ_KEY[:8]}")

# groq_client = Groq(api_key=GROQ_KEY)

if not GROQ_KEY:
    raise ValueError("GROQ_API_KEY is not set in environment variables")
groq_client = Groq(api_key=GROQ_KEY)


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
async def query_memory(request: QueryRequest):
    try:
        question_embedding = embed_text([request.question])[0]
        results = search_chunks(question_embedding, limit=5)

        if not results:
            return {"answer": "I don't have any memories about that yet.", "sources": []}

        context = "\n\n".join([
            f"From {r['url']}:\n{r['text']}"
            for r in results
        ])

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