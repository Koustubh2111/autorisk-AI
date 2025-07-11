from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text
from pypdf import PdfReader
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()
print(os.getenv('PGUSER'))
# Load environment variables for Postgres connection
db_url = f"postgresql+psycopg2://{os.getenv('PGUSER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
engine = create_engine(db_url)

def load_and_chunk_pdf(file_path):
    reader = PdfReader(file_path)
    raw_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(raw_text)
    return chunks

model = SentenceTransformer("all-MiniLM-L6-v2")

def store_chunks_to_pgvector(chunks, table="policy_chunks"):
    with engine.connect() as conn:
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id SERIAL PRIMARY KEY,
                chunk TEXT,
                embedding VECTOR(384)
            );
        """))

        for chunk in chunks:
            embedding = model.encode(chunk).astype(np.float32).tolist()
            conn.execute(
                text(f"INSERT INTO {table} (chunk, embedding) VALUES (:chunk, :embedding)"),
                {"chunk": chunk, "embedding": embedding}
            )
        conn.commit()

if __name__ == "__main__":
    chunks = load_and_chunk_pdf("embeddings/data/sample_policy.pdf")
    store_chunks_to_pgvector(chunks)
    print(f"Ingested {len(chunks)} chunks into pgvector.")
