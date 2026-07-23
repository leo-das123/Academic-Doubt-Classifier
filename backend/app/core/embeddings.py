"""
Embedding Service

Provides a singleton wrapper around the SentenceTransformer
embedding model.

The model is loaded only once and reused throughout the
application to reduce startup time and memory usage.
"""

from sentence_transformers import SentenceTransformer

from app.config import (
    EMBEDDING_MODEL,
    EMBEDDING_BATCH_SIZE,
)


class EmbeddingService:
    """
    Singleton service responsible for generating
    semantic embeddings.
    """

    _model = None

    @classmethod
    def load_model(cls):
        """
        Load the embedding model only once.
        """

        if cls._model is None:

            print("=" * 60)
            print("Loading Embedding Model...")
            print(f"Model : {EMBEDDING_MODEL}")
            print("=" * 60)

            cls._model = SentenceTransformer(
                EMBEDDING_MODEL
            )

            print("Embedding Model Loaded Successfully.\n")

        return cls._model

    @classmethod
    def generate(cls, text: str):
        """
        Generate an embedding for a single text.
        """

        model = cls.load_model()

        return model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    @classmethod
    def generate_batch(cls, texts: list[str]):
        """
        Generate embeddings for multiple texts.
        Used while building the FAISS index.
        """

        model = cls.load_model()

        return model.encode(
            texts,
            batch_size=EMBEDDING_BATCH_SIZE,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )