# MindMesh API Reference

This is a quick reference for the MindMesh endpoints. For full interactive testing, run the server and visit the auto-generated Swagger UI at `http://127.0.0.1:8000/docs`.

---

## Authentication

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/register` | No | Creates a new user. Expects `email` and `password` in JSON body. Returns a JWT access token. |
| `POST` | `/login` | No | Authenticates a user. Expects `username` (email) and `password` as form-data. Returns a JWT access token. |

---

## Articles & Documents

All endpoints below require a valid JWT token passed in the header: `Authorization: Bearer <token>`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/save` | Saves a URL. Automatically extracts text using `trafilatura` and indexes it into the vector database. |
| `POST` | `/upload-pdf` | Uploads a PDF file (`multipart/form-data`). Extracts text immediately and indexes it via a background task. |
| `GET` | `/article/{article_id}` | Retrieves metadata and extracted text for a specific article. Fails with 404 if the article doesn't belong to the authenticated user. |

---

## Search & AI

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/search?query=...` | Standard full-text search. Returns articles where the title or extracted text contains the query string (SQL ILIKE). |
| `GET` | `/ask?query=...` | Semantic search + RAG. Embeds the query, retrieves the top 5 most relevant chunks from the user's saved content, and uses Gemini to generate a synthesized answer. Returns the answer and source list. |
