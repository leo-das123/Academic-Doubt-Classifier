from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL


class EmbeddingModel:

    def __init__(self):

        print("=" * 50)
        print("Loading Embedding Model...")
        print("=" * 50)

        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

        print("Embedding Model Loaded Successfully.\n")

    def generate(self, text: str):

        return self.model.encode(
            text,
            convert_to_numpy=True
        )


embedding_model = EmbeddingModel()