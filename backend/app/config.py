"""
Central Configuration

Every module should import configuration
from this file instead of hardcoding values.
"""

import os

from dotenv import load_dotenv

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

# ==========================================================
# Gemini Configuration
# ==========================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "qwen3:4b"
)

# ==========================================================
# Embedding Configuration
# ==========================================================

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

# ==========================================================
# PDF Chunking
# ==========================================================

CHUNK_SIZE = int(
    os.getenv("CHUNK_SIZE", 500)
)

CHUNK_OVERLAP = int(
    os.getenv("CHUNK_OVERLAP", 100)
)

# ==========================================================
# Retrieval
# ==========================================================

TOP_K = int(
    os.getenv("TOP_K", 5)
)

# ==========================================================
# Directories
# ==========================================================

PDF_DIRECTORY = os.getenv(
    "PDF_DIRECTORY",
    "app/data/pdfs"
)

VECTOR_DB_PATH = os.getenv(
    "VECTOR_DB_PATH",
    "app/data/vector_db"
)

if __name__ == "__main__":

    print("=" * 60)

    print("Google API Key :", GOOGLE_API_KEY[:10] + "...")

    print("Model          :", MODEL_NAME)

    print("Embedding      :", EMBEDDING_MODEL)

    print("Chunk Size     :", CHUNK_SIZE)

    print("Chunk Overlap  :", CHUNK_OVERLAP)

    print("Top K          :", TOP_K)

    print("PDF Directory  :", PDF_DIRECTORY)

    print("Vector DB      :", VECTOR_DB_PATH)

    print("=" * 60)