"""
Retriever

Retrieves the most relevant knowledge chunks from the
FAISS vector database.

Responsibilities
----------------
1. Generate query embeddings.
2. Search the vector database.
3. Filter low-similarity results.
4. Remove duplicate page references.
5. Return the best chunks for context building.
"""

from app.config import (
    SIMILARITY_THRESHOLD,
    MAX_CONTEXT_CHUNKS,
)

from app.core.embeddings import EmbeddingService
from app.core.vector_store import VectorStore


class Retriever:
    """
    Semantic retriever for the Academic Doubt Classifier.
    """

    def __init__(self):

        self.vector_store = VectorStore()
        self.vector_store.load()

    # =====================================================
    # Retrieve Relevant Chunks
    # =====================================================

    def retrieve(
        self,
        question: str
    ):
        """
        Retrieve the most relevant chunks for a question.
        """

        # Generate query embedding
        query_embedding = EmbeddingService.generate(
            question
        )

        # Search vector database
        retrieved = self.vector_store.search(
            query_embedding
        )

        # Remove weak matches
        filtered = self._filter_similarity(
            retrieved
        )

        # Remove duplicate page references
        filtered = self._remove_duplicates(
            filtered
        )

        # Keep only the best context chunks
        # Keep only the best context chunks
        accepted = filtered[:MAX_CONTEXT_CHUNKS]

        return {
            "retrieved": retrieved,
            "accepted": accepted
        }

    # =====================================================
    # Similarity Filtering
    # =====================================================

    def _filter_similarity(
        self,
        results
    ):
        """
        Remove results below the similarity threshold.
        """

        return [

            item

            for item in results

            if item["similarity_score"]
            >= SIMILARITY_THRESHOLD

        ]

    # =====================================================
    # Duplicate Removal
    # =====================================================

    def _remove_duplicates(
        self,
        results
    ):
        """
        Remove duplicate page references while preserving
        ranking order.

        A page is uniquely identified by:

            (source PDF, page number)
        """

        unique = []

        seen = set()

        for item in results:

            key = (

                item["source"],

                item["page"]

            )

            if key in seen:
                continue

            seen.add(key)

            unique.append(item)

        return unique


   


# ==========================================================
# Module Test
# ==========================================================

if __name__ == "__main__":

    retriever = Retriever()

    print("=" * 60)
    print("Retriever Module Ready")
    print("=" * 60)