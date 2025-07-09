import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel #Input data validation models
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

app = FastAPI(title="AutoRiskAI Semantic Search API")

# Load embedding model once at startup
model = SentenceTransformer("all-MiniLM-L6-v2")

# Setup DB connection
db_url = (
    f"postgresql+psycopg2://{os.getenv('PGUSER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('PGHOST')}:"
    f"{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
)
engine = create_engine(db_url)

# Pydantic model for query input
class QueryRequest(BaseModel):
    """Defines the JSON body for search endpoint"""
    query: str
    top_k: int = 5

@app.post("/search")
def semantic_search(request: QueryRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query text is required.")

    # Create embedding for query
    query_embedding = model.encode(request.query).tolist()

    # Query DB for similar chunks
    with engine.connect() as conn:
        sql = text(
            """
            SELECT id, chunk, embedding <-> (:query_embedding)::vector AS distance
            FROM policy_chunks
            ORDER BY distance ASC
            LIMIT :top_k;
            """
        )
        result = conn.execute(sql, {"query_embedding": query_embedding, "top_k": request.top_k})
        matches = result.fetchall()

    # Format response
    response = [
        {"id": row.id, "chunk": row.chunk, "distance": row.distance}
        for row in matches
    ]

    return {"query": request.query, "results": response}
