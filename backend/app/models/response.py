"""
Response Models

Defines all API response schemas used by the
Academic Doubt Classifier.

Every response returned by the backend should conform
to these Pydantic models, ensuring consistency,
validation, and clear communication with the frontend.
"""

from pydantic import BaseModel, Field
from typing import List


# ==========================================================
# Classification Result
# ==========================================================

class Classification(BaseModel):
    """
    Academic classification predicted by the LLM.
    """

    subject: str = Field(
        ...,
        description="Predicted academic subject."
    )

    topic: str = Field(
        ...,
        description="Predicted topic within the subject."
    )

    subtopic: str = Field(
        ...,
        description="Predicted subtopic."
    )

    difficulty: str = Field(
        ...,
        description="Estimated difficulty level."
    )


# ==========================================================
# Reference Information
# ==========================================================

class Reference(BaseModel):
    """
    Represents a relevant page retrieved from the
    knowledge base.
    """

    source: str = Field(
        ...,
        description="Source PDF filename."
    )

    page: int = Field(
        ...,
        ge=1,
        description="Page number."
    )

    similarity_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Semantic similarity score."
    )


# ==========================================================
# Retrieval Information
# ==========================================================

class RetrievalInfo(BaseModel):
    """
    Information about the retrieval stage.
    """

    retrieved_chunks: int = Field(
        ...,
        ge=0,
        description="Total chunks returned by FAISS."
    )

    accepted_chunks: int = Field(
        ...,
        ge=0,
        description="Chunks remaining after filtering."
    )

    similarity_threshold: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Similarity threshold used."
    )


# ==========================================================
# Final API Response
# ==========================================================

class ClassificationResponse(BaseModel):
    """
    Final response returned to the frontend.
    """

    question: str = Field(
        ...,
        description="Original student question."
    )

    classification: Classification

    retrieval: RetrievalInfo

    references: List[Reference]

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall confidence score."
    )