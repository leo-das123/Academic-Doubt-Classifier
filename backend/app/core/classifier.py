"""
Academic Classifier

Main orchestration pipeline for the
Academic Doubt Classifier.

Pipeline
--------
Question
    ↓
Preprocessing
    ↓
Semantic Retrieval
    ↓
Context Building
    ↓
LLM Classification
    ↓
Confidence Scoring
    ↓
Structured API Response
"""

import logging

from app.config import SIMILARITY_THRESHOLD

from app.core.preprocess import TextPreprocessor
from app.core.retriever import Retriever
from app.core.context_builder import ContextBuilder
from app.core.llm_classifier import llm_classifier
from app.core.retrieval_scorer import retrieval_scorer

logger = logging.getLogger(__name__)


class AcademicClassifier:
    """
    Coordinates the complete academic
    doubt classification pipeline.
    """

    def __init__(self):

        self.retriever = Retriever()

    # ======================================================
    # Public API
    # ======================================================

    def classify(
        self,
        question: str
    ):
        """
        Classify an academic doubt.
        """

        # ----------------------------------------------
        # Preserve Original Question
        # ----------------------------------------------

        original_question = question

        # ----------------------------------------------
        # Preprocess
        # ----------------------------------------------

        cleaned_question = TextPreprocessor.clean(
            original_question
        )

        # ----------------------------------------------
        # Retrieve Knowledge
        # ----------------------------------------------

        retrieval_result = self.retriever.retrieve(
            cleaned_question
        )

        retrieved_chunks = retrieval_result["retrieved"]

        accepted_chunks = retrieval_result["accepted"]

        # ----------------------------------------------
        # Build Context
        # ----------------------------------------------

        context = ContextBuilder.build(
            accepted_chunks
        )

        prompt = ContextBuilder.build_prompt(

            question=original_question,

            context=context

        )

        # ----------------------------------------------
        # LLM Classification
        # ----------------------------------------------

        classification = llm_classifier.classify(
            prompt
        )

        # ----------------------------------------------
        # Confidence
        # ----------------------------------------------

        confidence = retrieval_scorer.calculate(
            accepted_chunks
        )

        # ----------------------------------------------
        # References
        # ----------------------------------------------

        references = []

        for chunk in accepted_chunks:

            references.append({

                "source": chunk["source"],

                "page": chunk["page"],

                "similarity_score": round(

                    chunk["similarity_score"],

                    3

                ),

                "preview": chunk["text"][:150]

            })

        # ----------------------------------------------
        # Retrieval Information
        # ----------------------------------------------

        retrieval = {

            "retrieved_chunks": len(

                retrieved_chunks

            ),

            "accepted_chunks": len(

                accepted_chunks

            ),

            "similarity_threshold": SIMILARITY_THRESHOLD

        }

        # ----------------------------------------------
        # Logging
        # ----------------------------------------------

        logger.info("=" * 60)
        logger.info("Academic Classification Completed")
        logger.info("=" * 60)

        logger.info(

            "Question : %s",

            original_question

        )

        logger.info(

            "Retrieved : %d",

            len(retrieved_chunks)

        )

        logger.info(

            "Accepted : %d",

            len(accepted_chunks)

        )

        logger.info(

            "Confidence : %.3f",

            confidence

        )

        # ----------------------------------------------
        # Final Response
        # ----------------------------------------------

        return {

            "question": original_question,

            "classification": classification,

            "retrieval": retrieval,

            "references": references,

            "confidence": round(

                confidence,

                3

            )

        }


# ======================================================
# Singleton
# ======================================================

academic_classifier = AcademicClassifier()


# ======================================================
# Module Test
# ======================================================

if __name__ == "__main__":

    result = academic_classifier.classify(

        "What is Deadlock?"

    )

    from pprint import pprint

    pprint(result)