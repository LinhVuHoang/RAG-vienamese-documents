from src.Embedding.embedding import model,embed
from src.Store.store import search
from src.config.config import BATCH_SIZE


def retrieve(query: str, top_k: int=5):
    #B1: Query --> Embedding
    
    query_vector = embed([query],BATCH_SIZE,model)[0]
    
    #B2: Search --> Top-K chunks
    
    results = search(query_vector, top_k)
    
    return results