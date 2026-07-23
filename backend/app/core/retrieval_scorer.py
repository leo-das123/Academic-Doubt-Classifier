"""
Retrieval Scorer

Computes the confidence score of a classification
based on semantic retrieval quality.

Responsibilities
----------------
1. Calculate retrieval confidence.
2. Provide retrieval statistics.
3. Handle empty retrieval results.

This module does NOT:
- perform retrieval
- call the LLM
- classify questions
"""

from statistics import mean


class RetrievalScorer:
    """
    Computes confidence scores using retrieved chunks.
    """

    @staticmethod
    def calculate(retrieved_chunks):
        """
        Calculate retrieval confidence.

        Parameters
        ----------
        retrieved_chunks : list

        Returns
        -------
        float
            Confidence score between 0.0 and 1.0
        """

        if not retrieved_chunks:
            return 0.0

        scores = [

            chunk["similarity_score"]

            for chunk in retrieved_chunks

            if "similarity_score" in chunk

        ]

        if not scores:
            return 0.0

        confidence = mean(scores)

        confidence = max(

            0.0,

            min(

                confidence,

                1.0

            )

        )

        return round(
            confidence,
            3
        )

    # ======================================================
    # Retrieval Statistics
    # ======================================================

    @staticmethod
    def statistics(
        retrieved_chunks
    ):
        """
        Return retrieval statistics.
        """

        if not retrieved_chunks:

            return {

                "retrieved_chunks": 0,

                "average_similarity": 0.0,

                "highest_similarity": 0.0,

                "lowest_similarity": 0.0

            }

        scores = [

            chunk["similarity_score"]

            for chunk in retrieved_chunks

        ]

        return {

            "retrieved_chunks": len(retrieved_chunks),

            "average_similarity": round(
                mean(scores),
                3
            ),

            "highest_similarity": round(
                max(scores),
                3
            ),

            "lowest_similarity": round(
                min(scores),
                3
            )

        }


# ======================================================
# Singleton
# ======================================================

retrieval_scorer = RetrievalScorer()


# ======================================================
# Module Test
# ======================================================

if __name__ == "__main__":

    sample = [

        {

            "similarity_score": 0.95

        },

        {

            "similarity_score": 0.91

        },

        {

            "similarity_score": 0.88

        }

    ]

    print(

        "Confidence :",

        retrieval_scorer.calculate(sample)

    )

    print(

        retrieval_scorer.statistics(sample)

    )