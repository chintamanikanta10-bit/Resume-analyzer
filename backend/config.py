"""
config.py

Purpose:
- Load environment variables
- Configure the Gemini API
- Initialize the embedding model
- Define important project paths
"""

import os
from pathlib import Path

from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-production-use-a-long-random-secret-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
MAX_UPLOAD_SIZE_BYTES = int(os.getenv("MAX_UPLOAD_SIZE_BYTES", str(10 * 1024 * 1024)))
MAX_PAGES_PER_PDF = int(os.getenv("MAX_PAGES_PER_PDF", "20"))
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "30"))
RATE_LIMIT_BURST = int(os.getenv("RATE_LIMIT_BURST", "10"))
ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://127.0.0.1:4173").split(",") if origin.strip()]

# ----------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------

load_dotenv()

# ----------------------------------------------------
# Project Paths
# ----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_FOLDER = BASE_DIR / "uploads"
VECTOR_DB_PATH = BASE_DIR / "database" / "chroma_db"
USER_DB_PATH = BASE_DIR / "database" / "users.sqlite3"

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)
USER_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------
# Gemini API
# ----------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Please add it to the .env file."
    )

_LLM_MODEL = None

def get_llm_model():
    global _LLM_MODEL
    if _LLM_MODEL is None:
        logger.info("Initializing Gemini GenerativeModel (Lazy Load)...")
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        _LLM_MODEL = genai.GenerativeModel(
            model_name="models/gemini-3.5-flash"
        )
    return _LLM_MODEL

# ----------------------------------------------------
# Embedding Model
# ----------------------------------------------------

_EMBEDDING_MODEL = None

def get_embedding_model():
    global _EMBEDDING_MODEL
    if _EMBEDDING_MODEL is None:
        logger.info("Initializing HuggingFaceEmbeddings (Lazy Load)...")
        from langchain_huggingface import HuggingFaceEmbeddings
        _EMBEDDING_MODEL = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _EMBEDDING_MODEL

# ----------------------------------------------------
# RAG Configuration
# ----------------------------------------------------

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

TOP_K_RESULTS = 4

# ----------------------------------------------------
# Prompt
# ----------------------------------------------------

SYSTEM_PROMPT = """
You are an AI Tutor.

Use BOTH:

1. The retrieved document context.
2. The previous conversation.

When answering:

- Prefer the retrieved document whenever it contains the required information.
- If the user asks a follow-up question like "Explain it", "Give an example", or "Can you simplify that?", use the previous conversation to understand what "it" refers to.
- If neither the retrieved context nor the conversation contains the answer, reply:

"I couldn't find that information in the uploaded document."

Always explain clearly and simply.
"""