# MindMesh Architecture & Internals

This document explains the system design, data flow, and technical decisions behind the MindMesh backend.

## Data Flow & Core Processes

### 1. Authentication & Security (`auth.py`)

* **Flow:** Users register with an email and password. Passwords are hashed using `bcrypt` (with a strict 72-byte limit enforced to prevent hashing errors).
* **Tokens:** Successful login issues a JSON Web Token (JWT) valid for 7 days.
* **Route Protection:** Protected endpoints inject the `get_current_user` dependency, ensuring the token is valid and appending the `user_id` to all subsequent database and vector store queries.

### 2. Document Ingestion & Extraction (`extraction.py`)

* **Web Pages:** Handled by `trafilatura`. It strips out HTML boilerplate, navigation menus, and ads, returning clean text.
* **PDFs:** Handled by `PyMuPDF` (`fitz`). It iterates through PDF pages and extracts text from the byte stream directly in memory.
* **Asynchronous Processing:** To keep the API snappy, heavy tasks (like vector embedding) for PDF uploads are offloaded to FastAPI's `BackgroundTasks`.

### 3. Vector Indexing (`vector_store.py`)

* **Chunking:** Extracted text is split using `RecursiveCharacterTextSplitter` into 1000-character chunks with a 200-character overlap. This ensures semantic context isn't lost between boundaries.
* **Embedding:** Chunks are passed through the `all-MiniLM-L6-v2` local model via `sentence-transformers`, converting text into high-dimensional vectors.
* **Storage:** Vectors are stored in a persistent ChromaDB instance (`./chroma_db`).
* **Data Isolation:** Every chunk is tagged with a `user_id` in its metadata. This is a critical security measure to ensure users only query their own data.

### 4. Retrieval-Augmented Generation (RAG) (`llm.py`)

* **Search:** When a user queries `/ask`, the query is embedded and searched against ChromaDB. The `where={"user_id": user_id}` filter guarantees cross-user data isolation.
* **Generation:** The top 5 matching chunks are concatenated into a strict prompt. Google's Gemini 2.5 Flash model is instructed via `system_instruction` to answer *only* using the provided context and to refuse if the answer is missing.

---

## BUT WHY?

* **FastAPI:** Chosen for its native asynchronous support, automatic Swagger UI documentation, and Pydantic validation.
* **ChromaDB over PGVector:** ChromaDB runs entirely locally in-memory/on-disk without needing complex PostgreSQL extensions or separate Docker containers for the vector store.
* **MiniLM-L6-v2:** An extremely fast and lightweight embedding model. It runs well on standard CPUs without requiring a dedicated GPU, making the backend highly portable.
* **Trafilatura over BeautifulSoup:** BeautifulSoup requires manually writing rules for different websites. Trafilatura is specifically designed to heuristically find the main content body of articles and blog posts.
