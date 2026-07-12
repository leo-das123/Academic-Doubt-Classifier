# Academic Doubt Classifier

Academic Doubt Classifier is a Retrieval-Augmented Generation (RAG) application that classifies academic questions into structured metadata including subject, topic, subtopic, and difficulty.

The system retrieves relevant knowledge from academic documents using semantic search with Sentence Transformers and FAISS, then performs structured classification using a locally hosted Qwen3 language model through Ollama. The application consists of a React frontend and a FastAPI backend communicating through a REST API.

---

## Features

- Retrieval-Augmented Generation (RAG) pipeline
- Semantic document retrieval using FAISS
- Sentence Transformer embeddings
- Local LLM inference using Ollama (Qwen3)
- Academic question classification
- Subject, topic, subtopic and difficulty prediction
- Reference page extraction
- React frontend
- FastAPI backend
- Responsive user interface

---

## System Architecture

```
                           Academic Question
                                   │
                                   ▼
                        React Frontend (Vite)
                                   │
                             REST API Request
                                   │
                                   ▼
                           FastAPI Backend
                                   │
                     Question Preprocessing
                                   │
                                   ▼
                   Sentence Transformer Embedding
                                   │
                                   ▼
                      FAISS Vector Similarity Search
                                   │
                    Top-K Knowledge Retrieval
                                   │
                                   ▼
                     Qwen3 (Ollama Local LLM)
                                   │
                    Structured Classification
                                   │
                                   ▼
                          JSON API Response
                                   │
                                   ▼
                         React User Interface
```

---

## Technology Stack

### Frontend

- React
- Vite
- Tailwind CSS
- JavaScript

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

### Artificial Intelligence

- Ollama
- Qwen3
- Sentence Transformers
- FAISS
- PyMuPDF

---

## Project Structure

```
Academic-Doubt-Classifier/

├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── indexing/
│   │   ├── services/
│   │   ├── config.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── README.md
├── .gitignore
└── requirements.txt
```

---

## Prerequisites

Before running the project, ensure the following software is installed.

- Python 3.10 or later
- Node.js 20 or later
- npm
- Ollama

---

## Installation

### Clone the repository

```bash
git clone https://github.com/leo-das123/Academic-Doubt-Classifier.git

cd Academic-Doubt-Classifier
```

---

### Backend

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the environment.

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install Python dependencies.

```bash
pip install -r requirements.txt
```

---

### Frontend

Navigate to the frontend directory.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

---

## Ollama Setup

Install Ollama from

https://ollama.com/download

Download the required model.

```bash
ollama pull qwen3:8b
```

Verify the model.

```bash
ollama list
```

---

## Configuration

Create a `.env` file inside the backend directory.

Example:

```env
MODEL_NAME=qwen3:8b

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

CHUNK_SIZE=500

CHUNK_OVERLAP=100

TOP_K=5
```

Store academic PDF files inside

```
backend/app/data/pdfs/
```

Build the vector database before starting the application.

---

## Running the Application

### Start Ollama

```bash
ollama serve
```

---

### Start Backend

```bash
cd backend

uvicorn app.main:app --reload
```

Backend runs on

```
http://localhost:8000
```

Swagger documentation

```
http://localhost:8000/docs
```

---

### Start Frontend

```bash
cd frontend

npm run dev
```

Frontend runs on

```
http://localhost:5173
```

---

## API

### POST

```
/api/classify
```

### Request

```json
{
    "question": "What is MapReduce?"
}
```

### Response

```json
{
    "question": "What is MapReduce?",
    "classification": {
        "subject": "Big Data",
        "topic": "MapReduce",
        "subtopic": "",
        "difficulty": "Easy",
        "confidence": 0.95
    },
    "references": [
        {
            "page": 36,
            "distance": 0.48
        }
    ]
}
```

---

## Retrieval Pipeline

```
PDF Documents

      │

      ▼

Text Extraction

      │

      ▼

Chunk Generation

      │

      ▼

Sentence Embeddings

      │

      ▼

FAISS Index

      │

      ▼

Similarity Search

      │

      ▼

Top-K Context

      │

      ▼

Qwen3 (Ollama)

      │

      ▼

Structured Classification
```

---

## Current Capabilities

- Academic question classification
- Semantic retrieval
- Local language model inference
- Structured JSON output
- Reference page extraction
- Responsive frontend
- REST API integration

---

## Roadmap

### Phase 1

- [x] React frontend
- [x] FastAPI backend
- [x] RAG pipeline
- [x] PDF indexing
- [x] FAISS retrieval
- [x] Ollama integration
- [x] Structured classification

### Phase 2

- [ ] Chat history
- [ ] Multi-turn conversations
- [ ] PDF upload interface
- [ ] Streaming responses
- [ ] Citation preview
- [ ] Loader animations
- [ ] Improved UI

### Phase 3

- [ ] Authentication
- [ ] Subject management
- [ ] Cloud deployment
- [ ] Docker support
- [ ] API versioning
- [ ] Monitoring
- [ ] Benchmark evaluation

---

## Notes

Large academic PDF files and generated vector databases are intentionally excluded from version control.

Populate the following directories before indexing documents.

```
backend/app/data/pdfs/
```

Generated vector indexes will be created in

```
backend/app/data/vector_db/
```

---

## License

This project is licensed under the MIT License.
