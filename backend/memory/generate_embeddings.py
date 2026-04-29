import os
from openai import OpenAI

# Initialize Gemini client for embeddings (Fast Path)
_client = None

def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            _client = OpenAI(
                api_key=api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
    return _client

def _generate_sync(strings: list[str]):
    """Generates embeddings using Google's Cloud API (Blazing fast)."""
    client = _get_client()
    if not client:
        print("⚠️ GEMINI_API_KEY not found. Embeddings disabled.")
        return []

    try:
        response = client.embeddings.create(
            model="text-embedding-004",
            input=strings
        )
        # Extract embeddings from response
        return [data.embedding for data in response.data]
    except Exception as e:
        print(f"⚠️ Google Embedding API error: {e}")
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
