from fastapi import APIRouter
from pydantic import BaseModel

from app.core.classifier import AcademicClassifier

router = APIRouter()


# ----------------------------
# Request Model
# ----------------------------
class DoubtRequest(BaseModel):
    question: str


# ----------------------------
# Response Model
# ----------------------------
class Reference(BaseModel):

    page: int

    distance: float


class Classification(BaseModel):

    subject: str

    topic: str | None

    subtopic: str | None

    difficulty: str | None

    confidence: float


class ClassificationResponse(BaseModel):

    question: str

    classification: Classification

    references: list[Reference]


# ----------------------------
# Classification Endpoint
# ----------------------------
@router.post("/classify", response_model=ClassificationResponse)
async def classify_doubt(request: DoubtRequest):

    result = AcademicClassifier.classify(request.question)

    return ClassificationResponse(**result)