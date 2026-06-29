# 🧠 Second Brain — AI-Powered Personal Memory System

An AI-powered system that passively captures your browsing history, PDFs, and notes, then lets you query everything you've ever read using natural language — powered by RAG (Retrieval Augmented Generation).

## 🚀 Live Demo

- **Frontend:** [second-brain-orpin-xi.vercel.app](https://second-brain-orpin-xi.vercel.app)
- **Backend API:** [second-brain-production-0011.up.railway.app](https://second-brain-production-0011.up.railway.app)

## ✨ Features

- **Passive Capture** — Chrome extension automatically captures every webpage you visit
- **Semantic Search** — Ask questions in natural language, get answers based on meaning (not just keywords)
- **RAG-Powered Answers** — Combines vector search with LLM to generate accurate, source-cited answers
- **Persistent Memory** — All data stored permanently in cloud vector database

## 🏗️ Architecture
Chrome Extension → FastAPI Backend → Embedding Model → Qdrant Vector DB

↓

Semantic Search

↓

Groq LLM (LLaMA 3.3)

↓

Next.js Chat UI

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js, React |
| Backend | FastAPI (Python) |
| Vector Database | Qdrant Cloud |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| LLM | Groq (LLaMA 3.3 70B) |
| Browser Extension | Chrome Extension (Manifest V3) |
| Deployment | Railway (backend) + Vercel (frontend) |

## 📁 Project Structure
second-brain/

├── backend/

│   ├── main.py

│   ├── routers/

│   │   ├── ingest.py      # Receives and processes webpage data

│   │   └── query.py       # Handles RAG query pipeline

│   ├── services/

│   │   ├── chunker.py     # Splits text into chunks

│   │   ├── embedder.py    # Generates embeddings

│   │   └── vector_store.py # Qdrant operations

│   └── db/

│       └── metadata.py    # SQLite operations

├── frontend/

│   └── app/

│       └── page.tsx       # Chat UI

└── extension/

├── manifest.json

├── content.js          # Extracts page content

└── background.js       # Sends data to backend

## ⚙️ How It Works

1. **Capture** — Chrome extension extracts text from every webpage you visit
2. **Process** — Backend chunks the text and generates embeddings using a local transformer model
3. **Store** — Embeddings stored in Qdrant Cloud with metadata (URL, timestamp, text)
4. **Query** — User asks a question → question gets embedded → Qdrant finds top-5 similar chunks
5. **Generate** — Retrieved chunks sent to Groq LLM as context → generates accurate, cited answer

## 🚧 Future Improvements

- Time-aware search ("what did I read last week?")
- PDF and YouTube transcript ingestion
- Knowledge graph visualization
- Multi-user authentication
- Proactive memory surfacing

## 📝 Local Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Load extension/ folder in chrome://extensions (Developer mode → Load unpacked)
```

## 👤 Author

Built by [Aditi Jain](https://github.com/aditijain1911)