import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

print("LOADING EMBEDDING MODEL...")

model = SentenceTransformer('all-MiniLM-L6-v2')

print("MODEL LOADED")

# Use environment variable for chroma path, default to ./chroma_db
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(
    name="mindmesh_articles"
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]
)

def index_article_in_vector_db(article_id: int, user_id: int, text: str, title: str, url: str):

    print("INDEX FUNCTION CALLED") #debugging ke liye hai, baad me hata dena
    
    if not text:
        print("NO TEXT FOUND")
        return

    print("TEXT LENGTH:", len(text))

    chunks = text_splitter.split_text(text)

    print("CHUNKS CREATED:", len(chunks))

    embeddings = model.encode(chunks).tolist()

    print("EMBEDDINGS CREATED")

    ids = [
        f"art_{article_id}_chunk_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [{
        "article_id": article_id, 
        "user_id": user_id, 
        "title": title or "Unknown", 
        "url": url
    } for _ in chunks]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )

    print(f"Successfully indexed {len(chunks)} chunks for article ID {article_id}")
    
def search_similar_chunks(query: str, user_id: int, n_results: int = 5):
    """
    Converts a query to an embedding and retrieves chunks strictly belonging to the requested user.
    """
    if not query:
        return None
        
    query_embedding = model.encode(query).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={"user_id": user_id} #hoping this to act as some privacy filter
    )
    
    if not results['documents'] or not results['documents'][0]:
        return None
        
    return {
        "chunks": results['documents'][0],
        "metadatas": results['metadatas'][0]
    }
