
# MindMesh Backend

A lightweight FastAPI backend for MindMesh. It handles saving articles (URLs, PDFs), extracting content, storing vector embeddings, and performing RAG-based Q&A using Google Gemini.
```
User → FastAPI → PostgreSQL (metadata + extracted text) + ChromaDB (embeddings) → Gemini → Response
```

## Tech Stack
- **Core:** FastAPI, PostgreSQL, JWT Auth
- **AI & Search:** ChromaDB, `sentence-transformers`, Google Gemini 2.5 Flash
- **Extraction:** `trafilatura` (web), `PyMuPDF` (PDF)

## Quick Start

1. **Install dependencies (preferrably in virtual env):**
   ```bash
   pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary trafilatura PyMuPDF chromadb sentence-transformers langchain-text-splitters google-generativeai python-jose[cryptography] passlib[bcrypt]

2. **Set your environment variables:**
```bash
export GEMINI_API_KEY="your-gemini-key"
export SECRET_KEY="your-secret-key"
```


3. **Configure the Database:**
Ensure PostgreSQL is running locally on port `5432` with a database named `mindmesh`. Update `database.py` with your credentials if necessary. Tables auto-generate on startup.
```
sudo service postgresql start
createdb mindmesh
```
5. **Run the server:**
```bash
uvicorn main:app --reload

```



*Once running, full API documentation and endpoint testing are available at `http://127.0.0.1:8000/docs`.*
