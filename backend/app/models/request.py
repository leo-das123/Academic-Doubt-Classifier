"""
Request Models

Defines all incoming API request schemas used by the
Academic Doubt Classifier.

Every request received by FastAPI is validated using
these Pydantic models before entering the backend
pipeline.
"""

from pydantic import BaseModel, Field, ConfigDict


class DoubtRequest(BaseModel):
    """
    Request model for classifying an academic doubt.
    """

    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Student's academic question."
    )

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )