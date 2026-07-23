"""
Classification API

Exposes the Academic Doubt Classification endpoint.

Responsibilities
----------------
1. Validate incoming requests.
2. Call the AcademicClassifier.
3. Return a structured API response.

This module contains NO business logic.
"""

from fastapi import APIRouter, HTTPException

from app.core.classifier import academic_classifier
from app.models.request import DoubtRequest
from app.models.response import ClassificationResponse

router = APIRouter(
    tags=["Academic Classifier"]
)


# ======================================================
# Classification Endpoint
# ======================================================

@router.post(
    "/classify",
    response_model=ClassificationResponse,
    summary="Classify an academic doubt",
    description="""
Classifies a student's academic question using
semantic retrieval and a local LLM.

Pipeline

Question
    ↓
Retrieval
    ↓
Context Building
    ↓
LLM Classification
    ↓
Confidence Scoring
"""
)
async def classify_doubt(
    request: DoubtRequest
):
    """
    Classify a student's academic doubt.
    """

    try:

        result = academic_classifier.classify(
            request.question
        )

        return ClassificationResponse(
            **result
        )

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=f"Classification failed: {str(error)}"

        )