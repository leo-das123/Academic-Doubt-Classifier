"""
Central Configuration

Every module in the project should import configuration
from this file instead of hardcoding values.

Changing the application's behaviour should require
editing only the .env file whenever possible.
"""

import os
from dotenv import load_dotenv

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

# ==========================================================
# Ollama Configuration
# ==========================================================

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "qwen3:8b"
)

# ==========================================================
# Embedding Configuration
# ==========================================================

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

EMBEDDING_BATCH_SIZE = int(
    os.getenv(
        "EMBEDDING_BATCH_SIZE",
        "32"
    )
)

# ==========================================================
# PDF Chunking Configuration
# ==========================================================

CHUNK_SIZE = int(
    os.getenv(
        "CHUNK_SIZE",
        "500"
    )
)

CHUNK_OVERLAP = int(
    os.getenv(
        "CHUNK_OVERLAP",
        "100"
    )
)

# ==========================================================
# Retrieval Configuration
# ==========================================================

MAX_RETRIEVALS = int(
    os.getenv(
        "MAX_RETRIEVALS",
        "15"
    )
)

MAX_CONTEXT_CHUNKS = int(
    os.getenv(
        "MAX_CONTEXT_CHUNKS",
        "6"
    )
)

SIMILARITY_THRESHOLD = float(
    os.getenv(
        "SIMILARITY_THRESHOLD",
        "0.55"
    )
)

# ==========================================================
# Context Builder Configuration
# ==========================================================

MAX_CONTEXT_CHARACTERS = int(
    os.getenv(
        "MAX_CONTEXT_CHARACTERS",
        "6000"
    )
)

# ==========================================================
# Storage Configuration
# ==========================================================

PDF_DIRECTORY = os.getenv(
    "PDF_DIRECTORY",
    "app/data/pdfs"
)

VECTOR_DB_PATH = os.getenv(
    "VECTOR_DB_PATH",
    "app/data/vector_db"
)

# ==========================================================
# Logging Configuration
# ==========================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

DEBUG = os.getenv(
    "DEBUG",
    "False"
).lower() == "true"

# ==========================================================
# Debug Information
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("Academic Doubt Classifier Configuration")
    print("=" * 70)

    print(f"Model Name              : {MODEL_NAME}")
    print(f"Embedding Model         : {EMBEDDING_MODEL}")
    print(f"Embedding Batch Size    : {EMBEDDING_BATCH_SIZE}")

    print()

    print(f"Chunk Size              : {CHUNK_SIZE}")
    print(f"Chunk Overlap           : {CHUNK_OVERLAP}")

    print()

    print(f"Max Retrievals          : {MAX_RETRIEVALS}")
    print(f"Max Context Chunks      : {MAX_CONTEXT_CHUNKS}")
    print(f"Similarity Threshold    : {SIMILARITY_THRESHOLD}")

    print()

    print(f"Max Context Characters  : {MAX_CONTEXT_CHARACTERS}")

    print()

    print(f"PDF Directory           : {PDF_DIRECTORY}")
    print(f"Vector Database Path    : {VECTOR_DB_PATH}")

    print()

    print(f"Log Level               : {LOG_LEVEL}")
    print(f"Debug Mode              : {DEBUG}")

    print("=" * 70)