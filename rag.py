import os
import textwrap
from pathlib import Path
import streamlit as st
import chromadb
from chromadb.config import Settings
from google import genai

# ── Constants ─────────────────────────────────────────────────────────────────
_EMBED_MODEL    = "gemini-embedding-2"
_COLLECTION     = "gordon_knowledge"
_CHUNK_SIZE     = 800       
_CHUNK_OVERLAP  = 80        
_TOP_K          = 3         
_KNOWLEDGE_FILE = Path(__file__).parent / "knowledge.txt"
_CHROMA_DIR     = Path(__file__).parent / ".chromadb"

# ── Dynamic Client Setup ──────────────────────────────────────────────────────
def _get_embed_client():
    api_key = st.session_state.get("google_api_key")
    if not api_key:
        try:
            api_key = st.secrets["google"]["api_key"]
        except Exception:
            pass
    if not api_key:
        import os
        api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        # Default fallback key
        api_key = "AIzaSyBBlh3szxTImAtUHx-VEF9ute2RbFmVezQ"
    return genai.Client(api_key=api_key)

_chroma = chromadb.PersistentClient(
    path=str(_CHROMA_DIR),
    settings=Settings(anonymized_telemetry=False),
)

# ── Internal helpers ──────────────────────────────────────────────────────────
def _chunk_text(text: str, size: int = _CHUNK_SIZE, overlap: int = _CHUNK_OVERLAP) -> list[str]:
    text   = " ".join(text.split())  
    chunks = []
    start  = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return [c for c in chunks if c.strip()]

def _embed(texts: list[str]) -> list[list[float]]:
    client = _get_embed_client()
    response = client.models.embed_content(
        model=_EMBED_MODEL,
        contents=texts,
    )
    return [e.values for e in response.embeddings]

# ── Public API ────────────────────────────────────────────────────────────────
def build_index(force: bool = False) -> None:
    collection = _chroma.get_or_create_collection(
        name=_COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )

    if collection.count() > 0 and not force:
        return 

    if not _KNOWLEDGE_FILE.exists():
        raise FileNotFoundError(f"knowledge.txt not found at {_KNOWLEDGE_FILE}.")

    raw    = _KNOWLEDGE_FILE.read_text(encoding="utf-8")
    chunks = _chunk_text(raw)
    vectors = _embed(chunks)
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.upsert(ids=ids, embeddings=vectors, documents=chunks)

def is_indexed() -> bool:
    try:
        col = _chroma.get_collection(_COLLECTION)
        return col.count() > 0
    except Exception:
        return False

def retrieve(query: str, top_k: int = _TOP_K) -> str:
    collection = _chroma.get_or_create_collection(
        name=_COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )

    if collection.count() == 0:
        return ""

    query_vector = _embed([query])[0]
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=min(top_k, collection.count()),
        include=["documents", "distances"],
    )

    chunks    = results["documents"][0]   
    distances = results["distances"][0]    

    if not chunks:
        return ""

    lines = []
    for i, (chunk, dist) in enumerate(zip(chunks, distances), start=1):
        similarity = round(1 - dist, 3)  
        lines.append(f"[Chunk {i} | similarity {similarity}]\n{chunk}")

    return "\n\n".join(lines)