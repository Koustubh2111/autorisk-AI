import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
import numpy as np


load_dotenv()

# Load embedding model (must match the one used in ingestion!)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Database setup
db_url = f"postgresql+psycopg2://{os.getenv('PGUSER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
engine = create_engine(db_url)

def search(query_text, top_k=5):
    # Step 1: Embed the query
    query_embedding = model.encode(query_text).tolist()  # Convert to Python list
    
    # Step 2: Search in DB using cosine similarity (pgvector's <-> operator)
    with engine.connect() as conn:
        
        result = conn.execute(
            text("""
                SELECT id, chunk, embedding <-> (:query_embedding)::vector AS distance
                FROM policy_chunks
                ORDER BY distance ASC
                LIMIT :top_k;
            """),
            {"query_embedding": query_embedding, "top_k": top_k}
        )
        matches = result.fetchall()

    print(f"\nTop {top_k} results for: \"{query_text}\"")
    for i, row in enumerate(matches, 1):
        print(f"\n#{i} - Distance: {row.distance:.4f}")
        print(row.chunk)

if __name__ == "__main__":
    user_query = input("Enter your question: ")
    search(user_query)
