"""
Vector Store

Provides an interface for creating, saving, loading,
and searching the FAISS vector database.

Responsibilities
----------------
- Create FAISS index
- Save index and metadata
- Load index and metadata
- Perform nearest-neighbor search

This module intentionally does NOT perform filtering,
ranking, prompt building, or classification.
"""

import pickle
from pathlib import Path

import faiss
import numpy as np

from app.config import (
    VECTOR_DB_PATH,
    MAX_RETRIEVALS,
)


class VectorStore:
    """
    Handles all interactions with the FAISS vector database.
    """

    def __init__(self):

        self.index = None
        self.metadata = []

        self.vector_db_path = Path(VECTOR_DB_PATH)
        self.vector_db_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.index_file = self.vector_db_path / "faiss_index.bin"
        self.metadata_file = self.vector_db_path / "metadata.pkl"

    # ======================================================
    # Create Index
    # ======================================================

    def create_index(
        self,
        embeddings,
        metadata
    ):
        """
        Create a new FAISS index from embeddings.
        """

        vectors = np.asarray(
            embeddings,
            dtype=np.float32
        )

        if vectors.ndim != 2:
            raise ValueError(
                "Embeddings must be a 2D array."
            )

        dimension = vectors.shape[1]

        # Cosine similarity using normalized embeddings
        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(vectors)

        self.metadata = metadata

        print("=" * 60)
        print("FAISS Index Created Successfully")
        print("=" * 60)
        print(f"Vectors   : {self.index.ntotal}")
        print(f"Dimension : {dimension}")
        print("=" * 60)

    # ======================================================
    # Save Index
    # ======================================================

    def save(self):
        """
        Save FAISS index and metadata.
        """

        if self.index is None:
            raise RuntimeError(
                "No FAISS index available to save."
            )

        faiss.write_index(
            self.index,
            str(self.index_file)
        )

        with open(
            self.metadata_file,
            "wb"
        ) as file:

            pickle.dump(
                self.metadata,
                file
            )

        print("Vector database saved successfully.")

    # ======================================================
    # Load Index
    # ======================================================

    def load(self):
        """
        Load FAISS index and metadata from disk.
        """

        if not self.index_file.exists():
            raise FileNotFoundError(
                f"Index not found: {self.index_file}"
            )

        if not self.metadata_file.exists():
            raise FileNotFoundError(
                f"Metadata not found: {self.metadata_file}"
            )

        self.index = faiss.read_index(
            str(self.index_file)
        )

        with open(
            self.metadata_file,
            "rb"
        ) as file:

            self.metadata = pickle.load(file)

        print("=" * 60)
        print("Vector Database Loaded Successfully")
        print("=" * 60)
        print(f"Vectors : {self.index.ntotal}")
        print(f"Metadata: {len(self.metadata)}")
        print("=" * 60)

    # ======================================================
    # Search
    # ======================================================

    def search(
        self,
        query_embedding,
        top_k=None
    ):
        """
        Search the FAISS index.

        Parameters
        ----------
        query_embedding : numpy.ndarray
            Query embedding.

        top_k : int, optional
            Number of nearest neighbors.

        Returns
        -------
        list
            Retrieved metadata with similarity scores.
        """

        if self.index is None:
            raise RuntimeError(
                "Vector database has not been loaded."
            )

        if top_k is None:
            top_k = MAX_RETRIEVALS

        query = np.asarray(
            [query_embedding],
            dtype=np.float32
        )

        scores, indices = self.index.search(
            query,
            top_k
        )

        results = []

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            if idx == -1:
                continue

            item = self.metadata[idx].copy()

            item["similarity_score"] = float(score)

            results.append(item)

        return results


# ======================================================
# Module Test
# ======================================================

if __name__ == "__main__":

    store = VectorStore()

    print("=" * 60)
    print("VectorStore Module Ready")
    print("=" * 60)