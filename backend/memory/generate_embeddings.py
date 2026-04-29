import os
import asyncio
import httpx

# We use the REST API directly since OpenAI-compatible endpoint 
# doesn't support embeddings yet.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def _generate_sync(strings: list[str]):
    """Generates embeddings using Google's REST API (Native)."""
    if not GEMINI_API_KEY:
        print("⚠️ GEMINI_API_KEY not found. Embeddings disabled.")
        return []

    url = f"https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:batchEmbedContents?key={GEMINI_API_KEY}"
    
    requests = [
        {
            "model": "models/text-embedding-004",
            "content": {"parts": [{"text": s}]}
        } for s in strings
    ]
    
    try:
        # We use a sync client here as it's wrapped in asyncio.to_thread
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(url, json={"requests": requests})
            resp.raise_for_status()
            data = resp.json()
            
            # Extract embeddings
            return [e["values"] for e in data.get("embeddings", [])]
    except Exception as e:
        print(f"⚠️ Google Embedding REST API error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return []

async def generate_embeddings(strings: list[str]):
    if not strings:
        return []
        
    # Run the CPU-bound embedding generation in a separate thread
    # so we don't block the FastAPI async loop and responses.
    embeddings = await asyncio.to_thread(_generate_sync, strings)
    
    # Ensure it's always a list of lists (handling single vs multiple strings)
    if len(embeddings) > 0 and not isinstance(embeddings[0], list):
        embeddings = [embeddings]
        
    return embeddings

if __name__ == "__main__":
    texts = [
        "Hello how are you",
        "I like Machine Learning"
    ]
    print(asyncio.run(generate_embeddings(texts)))
