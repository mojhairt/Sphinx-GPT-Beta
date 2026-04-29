"""
Migration script: Re-embed all existing memories with gemini-embedding-001.
Preserves all memory text/categories/dates — only regenerates the embeddings.

Usage:
  1. First, run this SQL in Supabase Dashboard:
     
     ALTER TABLE memories ALTER COLUMN embedding TYPE vector(3072);
     
     -- Also update the match_memories function:
     CREATE OR REPLACE FUNCTION match_memories(
       query_embedding vector(3072),
       match_user_id text,
       match_count int DEFAULT 5
     )
     RETURNS TABLE (
       id uuid,
       user_id text,
       memory_text text,
       categories text[],
       date text,
       similarity float
     )
     LANGUAGE plpgsql
     AS $$
     BEGIN
       RETURN QUERY
       SELECT
         m.id,
         m.user_id,
         m.memory_text,
         m.categories,
         m.date,
         1 - (m.embedding <=> query_embedding) AS similarity
       FROM memories m
       WHERE m.user_id = match_user_id
       ORDER BY m.embedding <=> query_embedding
       LIMIT match_count;
     END;
     $$;

  2. Then run this script:
     python migrate_embeddings.py
"""

import os
import sys
import time
import httpx
from dotenv import load_dotenv

# Load env from backend root
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def generate_embedding(text: str) -> list[float]:
    """Generate a single embedding using gemini-embedding-001."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key={GEMINI_API_KEY}"
    body = {
        "model": "models/gemini-embedding-001",
        "content": {"parts": [{"text": text}]}
    }
    resp = httpx.post(url, json=body, timeout=15.0)
    resp.raise_for_status()
    return resp.json()["embedding"]["values"]


def main():
    if not all([GEMINI_API_KEY, SUPABASE_URL, SUPABASE_KEY]):
        print("❌ Missing env vars (GEMINI_API_KEY, SUPABASE_URL, SUPABASE_KEY)")
        sys.exit(1)

    from supabase import create_client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Step 1: Fetch all existing memories (text only, no embedding needed)
    print("📖 Fetching all existing memories...")
    result = supabase.table("memories").select("id, user_id, memory_text, categories, date").execute()
    rows = result.data or []

    if not rows:
        print("ℹ️  No memories found. Nothing to migrate.")
        return

    print(f"📦 Found {len(rows)} memories to re-embed.\n")

    # Step 2: Re-embed each memory and update
    success = 0
    failed = 0

    for i, row in enumerate(rows):
        memory_id = row["id"]
        text = row["memory_text"]
        print(f"  [{i+1}/{len(rows)}] Re-embedding: \"{text[:60]}{'...' if len(text) > 60 else ''}\"")

        try:
            new_embedding = generate_embedding(text)
            
            # Update the row with the new embedding
            supabase.table("memories").update({
                "embedding": new_embedding
            }).eq("id", memory_id).execute()

            success += 1
            print(f"           ✅ Done ({len(new_embedding)} dims)")

        except Exception as e:
            failed += 1
            print(f"           ❌ Failed: {e}")

        # Small delay to respect rate limits
        time.sleep(0.3)

    print(f"\n{'='*50}")
    print(f"✅ Migration complete!")
    print(f"   Successful: {success}")
    print(f"   Failed:     {failed}")
    print(f"   Total:      {len(rows)}")


if __name__ == "__main__":
    main()
