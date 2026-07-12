from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.classify import router as classify_router


app = FastAPI(
    title="Academic Doubt Classifier API",
    description="AI-powered Academic Doubt Classification System",
    version="1.0.0"
)


# ----------------------------
# CORS Configuration
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # React (Vite)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Register API Routes
# ----------------------------
app.include_router(
    classify_router,
    prefix="/api",
    tags=["Academic Doubt Classifier"]
)


# ----------------------------
# Root Endpoint
# ----------------------------
@app.get("/")
def root():
    return {
        "message": "Academic Doubt Classifier API is running successfully."
    }