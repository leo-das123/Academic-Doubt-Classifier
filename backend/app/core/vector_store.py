import pickle
from pathlib import Path

import faiss
import numpy as np

from app.config import VECTOR_DB_PATH


class VectorStore:
    """
    Handles creation, saving, loading,
    and searching of the FAISS vector database.
    """

    def __init__(self):

        self.index = None

        self.metadata = []

        self.vector_db_path = Path(VECTOR_DB_PATH)

        self.vector_db_path.mkdir(parents=True, exist_ok=True)

        self.index_file = self.vector_db_path / "faiss_index.bin"

        self.metadata_file = self.vector_db_path / "metadata.pkl"

    # --------------------------------------------------
    # Create FAISS Index
    # --------------------------------------------------

    def create_index(self, embeddings, metadata):

        vectors = np.array(embeddings).astype("float32")

        dimension = vectors.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(vectors)

        self.metadata = metadata

        print("=" * 70)
        print("FAISS Index Created Successfully")
        print("=" * 70)
        print(f"Vectors : {self.index.ntotal}")
        print(f"Dimension : {dimension}")
        print("=" * 70)

    # --------------------------------------------------
    # Save Index
    # --------------------------------------------------

    def save(self):

        faiss.write_index(
            self.index,
            str(self.index_file)
        )

        with open(self.metadata_file, "wb") as file:

            pickle.dump(self.metadata, file)

        print("Vector Database Saved Successfully.")

    # --------------------------------------------------
    # Load Index
    # --------------------------------------------------

    def load(self):

        self.index = faiss.read_index(
            str(self.index_file)
        )

        with open(self.metadata_file, "rb") as file:

            self.metadata = pickle.load(file)

        print("Vector Database Loaded Successfully.")

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    def search(
        self,
        query_embedding,
        top_k=5
    ):

        query = np.array(
            [query_embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            query,
            top_k
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            item = self.metadata[index].copy()

            item["distance"] = float(distance)

            results.append(item)

        return results


# --------------------------------------------------
# Testing
# --------------------------------------------------

if __name__ == "__main__":

    print("VectorStore Module Ready.")