from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(title="SmartRoute API", version="0.1.0")

# CORS is important for the React Dashboard to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev, allow all. In prod, lock this down.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.post("/api/cache/clear")
async def clear_cache_endpoint():
    from app.core.cache import clear_cache
    from app.services.providers import STATS
    
    # 1. Clear Qdrant
    success = clear_cache()
    
    # 2. Reset In-Memory Stats
    STATS["requests"] = 0
    STATS["total_requests"] = 0 # specific key used in some logic
    STATS["cache_hits"] = 0
    STATS["cache_misses"] = 0
    STATS["total_savings"] = 0.0
    STATS["provider_groq"] = 0
    STATS["provider_local"] = 0
    STATS["latest_request"] = {
        "type": "Waiting...",
        "provider": "Waiting...",
        "timestamp": 0
    }
    
    return {"status": "success", "message": "Cache purged and stats reset"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
