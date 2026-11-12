import chromadb
from src.config.config import DB_DIR, COLLECTION
from src.logger import logger

client = chromadb.PersistentClient(path=str(DB_DIR))
collection = client.get_or_create_collection(
    COLLECTION, metadata={"hnsw:space": "cosine"}
)

logger.info(f"ChromaDB collection initialized: {COLLECTION}")

def add_chunks(chunks, vectors):
    collection.upsert(
        ids=[c.metadata["chunk_id"] for c in chunks],
        documents=[c.page_content for c in chunks],
        embeddings=vectors,
        metadatas=[c.metadata for c in chunks],
    )
    logger.info(f"Stored {len(chunks)} chunks into ChromaDB")

def search(query_vec, k=5):
    return collection.query(query_embeddings=[query_vec], n_results=k) # query input đã được embedding, trả về các chunk gần nhất với query_vec