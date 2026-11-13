from fastapi import FastAPI
from src.api.document_api import router as document_router
from src.api.chat_api import router as chat_router

app = FastAPI(
    title="Vietnamese Banking RAG API",
    description="API for indexing PDF documents into Vector Database",
    version="1.0.0"
)


app.include_router(
    document_router,
    prefix = "/api/v1",
    tags = ["Document"]
)
app.include_router(
    chat_router,
    prefix = "/api/v1",
    tags = ["Chat"]
)

@app.get("/")

def root():
    return {
        "message": "Vietnamese Banking RAG API is running"
    }