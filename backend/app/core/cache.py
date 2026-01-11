from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import json
import os
from app.core.config import settings

# Initialize Qdrant in Local Mode (saves to disk, no Docker needed)
# "location" argument creates a local database
client = QdrantClient(path="./qdrant_data") 

# Load embedding model (Small and fast)
# multi-qa-MiniLM-L6-cos-v1 is great for semantic search
print("Loading Embedding Model (this may take a moment first time)...")
embedding_model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

COLLECTION_NAME = "llm_cache_v1"

# Global flag to track if cache is active
CACHE_ENABLED = False

def init_cache():
    """Create collection if it doesn't exist"""
    global CACHE_ENABLED
    try:
        collections = client.get_collections()
        if COLLECTION_NAME not in [c.name for c in collections.collections]:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=384, # Output size of MiniLM-L6
                    distance=models.Distance.COSINE
                )
            )
            print(f"Created Qdrant collection: {COLLECTION_NAME}")
        CACHE_ENABLED = True
        print("✅ Cache System Initialized Successfully")
    except Exception as e:
        print(f"⚠️ Cache Initialization Failed: {e}")
        print("⚠️ Continuing without caching...")
        CACHE_ENABLED = False

def _get_prompt_text(messages: list) -> str:
    """Concatenate messages to form the search query"""
    return json.dumps(messages)

def check_cache(messages: list, threshold: float = 0.9):
    if not CACHE_ENABLED:
        return None
        
    try:
        prompt_text = _get_prompt_text(messages)
        vector = embedding_model.encode(prompt_text).tolist()
        
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=1
        )
        
        if results:
            best_match = results[0]
            if best_match.score >= threshold:
                print(f"🔥 Cache HIT! Score: {best_match.score}")
                return best_match.payload.get("response")
    except Exception as e:
        print(f"Error checking cache: {e}")
            
    print("🧊 Cache MISS")
    return None

def save_to_cache(messages: list, response: dict):
    if not CACHE_ENABLED:
        return

    try:
        prompt_text = _get_prompt_text(messages)
        vector = embedding_model.encode(prompt_text).tolist()
        
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=abs(hash(prompt_text)), # Simple deterministic ID
                    vector=vector,
                    payload={
                        "prompt": prompt_text,
                        "response": response
                    }
                )
            ]
        )
        print("Saved response to cache")
    except Exception as e:
        print(f"Error saving to cache: {e}")

def clear_cache():
    """Wipe the entire cache collection"""
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"🗑️ Deleted collection: {COLLECTION_NAME}")
        # Re-init immediately
        init_cache()
        return True
    except Exception as e:
        print(f"Error clearing cache: {e}")
        return False

# Initialize on module load
init_cache()
