import os
from pathlib import Path
from dotenv import load_dotenv

APP_DIR = Path(__file__).resolve().parent
BACKEND_ROOT = APP_DIR.parent
load_dotenv(dotenv_path=APP_DIR / ".env")

class Config:
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    VECTOR_DB_PATH = BACKEND_ROOT / "vectorstore"
    DATA_PATH = APP_DIR / "data" / "documents"

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # RAG Parameters
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 100
    RETRIEVAL_K = 4

config = Config()