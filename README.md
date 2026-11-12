# Vietnamese Banking RAG

A Retrieval-Augmented Generation (RAG) project for processing Vietnamese banking documents and preparing them for semantic search.

## 1. Overview

Vietnamese Banking RAG is a document processing system that allows users to upload PDF documents, extract their content, split the content into smaller chunks, convert chunks into vector embeddings, and store them in a vector database.

The project focuses on building the document ingestion and indexing pipeline as the foundation for a Vietnamese document question-answering system.

### Current Scope

- PDF document upload through REST API.
- PDF parsing and Markdown extraction.
- Structure-aware text chunking.
- Text embedding generation.
- Vector storage using ChromaDB.
- Logging and exception handling.

## 2. Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend API | FastAPI |
| Document Processing | PDF Parser |
| Text Chunking | LangChain Text Splitters |
| Embedding | Sentence Transformers |
| Vector Database | ChromaDB |
| Logging | Python Logging |
| API Testing | FastAPI Swagger UI |

## 3. System Architecture

```text
                  Client
                    |
                    | Upload PDF
                    v
              FastAPI Backend
                    |
                    v
             Document API Router
                    |
                    v
              Save PDF to RAW_DIR
                    |
                    v
            IndexingPipeline
                    |
          +---------+---------+
          |         |         |
          v         v         v
       Parsing   Chunking  Embedding
          |         |         |
          |         |         |
          +---------+---------+
                    |
                    v
               Store Layer
                    |
                    v
                ChromaDB
```

## 4. Project Structure

```text
Vietnamese-Banking-RAG/
│
├── data/
│   ├── raw/                  # Original uploaded PDF files
│   └── vectordb/             # Persistent ChromaDB storage
│
├── logs/                     # Application logs
│
├── src/
│   ├── api/
│   │   └── document_api.py   # PDF upload endpoint
│   │
│   ├── config/
│   │   └── config.py         # Project configuration
│   │
│   ├── Parsing/
│   │   └── parse_pdf.py      # PDF parsing
│   │
│   ├── Chunking/
│   │   └── chunking.py       # Markdown chunking
│   │
│   ├── Embedding/
│   │   └── embedding.py      # Embedding model and inference
│   │
│   ├── Store/
│   │   └── store.py          # ChromaDB operations
│   │
│   ├── Pipeline/
│   │   └── indexing_pipeline.py
│   │
│   ├── logger.py             # Logging configuration
│   ├── exception.py          # Custom exception handling
│   └── main.py               # FastAPI application
│
├── .env
├── requirements.txt
└── README.md
```

## 5. Configuration

The project uses a centralized configuration file to manage directory paths and processing parameters.

Example:

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT / "data" / "raw"
DB_DIR = ROOT / "data" / "vectordb"

COLLECTION = "banking_documents"

BATCH_SIZE = 16
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200
```

| Parameter | Description |
|---|---|
| `ROOT` | Project root directory |
| `RAW_DIR` | Directory for original PDF documents |
| `DB_DIR` | Persistent ChromaDB storage directory |
| `COLLECTION` | ChromaDB collection name |
| `BATCH_SIZE` | Number of texts processed per embedding batch |
| `CHUNK_SIZE` | Maximum target chunk size |
| `CHUNK_OVERLAP` | Overlapping characters between chunks |

## 6. Document Ingestion Pipeline

The indexing pipeline consists of four main stages.

### 6.1. PDF Parsing

**Input:** PDF file path.

**Output:** Extracted Markdown or text content.

```python
markdown_content = parse_pdf(pdf_path)
```

The parsing module extracts textual content from PDF documents and prepares it for downstream processing.

The extracted content is represented as Markdown when the parser can preserve document structure.

### 6.2. Text Chunking

**Input:** Markdown content.

**Output:** A list of document chunks.

The chunking module uses two splitting stages:

1. `MarkdownHeaderTextSplitter`: Splits content according to Markdown headings and preserves heading information in metadata.
2. `RecursiveCharacterTextSplitter`: Further divides long sections into smaller chunks.

Example configuration:

```python
chunk_size = 1500
chunk_overlap = 200
```

Each chunk contains:

- `page_content`: Text content.
- `metadata`: Source document, chunk ID, and heading information.

Example:

```python
{
    "page_content": "Banking service terms...",
    "metadata": {
        "source": "bank_terms.pdf",
        "chunk_id": "bank_terms.pdf-0",
        "h1": "Account Services",
        "h2": "Account Opening"
    }
}
```

### 6.3. Embedding Generation

**Input:** List of text chunks.

**Output:** List of numerical vectors.

The embedding module converts textual chunks into vector representations using a sentence embedding model.

```python
def embed(texts, batch_size, model):
    return model.encode(
        texts,
        batch_size=batch_size,
        normalize_embeddings=True,
        show_progress_bar=True
    ).tolist()
```

Key configurations:

- Batch processing to handle multiple chunks efficiently.
- Normalized embeddings for cosine similarity-based retrieval.
- Python list conversion for compatibility with ChromaDB.

### 6.4. Vector Storage

**Input:** Document chunks and their embeddings.

**Output:** Data stored in ChromaDB.

ChromaDB is initialized with persistent storage:

```python
client = chromadb.PersistentClient(
    path=str(DB_DIR)
)

collection = client.get_or_create_collection(
    name=COLLECTION,
    metadata={"hnsw:space": "cosine"}
)
```

The storage module uses `upsert()` to store:

| Field | Description |
|---|---|
| IDs | Unique chunk identifiers |
| Documents | Original chunk text |
| Embeddings | Vector representations |
| Metadatas | Source and heading information |

Using persistent storage allows indexed data to remain available after restarting the application.

## 7. Indexing Pipeline Implementation

The `IndexingPipeline` class orchestrates the four processing stages.

```python
class IndexingPipeline:

    def __init__(self):
        self.model = model

    def ingestion_pipeline(self, pdf_path: str):
        try:
            source = os.path.basename(pdf_path)

            # Step 1: PDF Parsing
            markdown_content = parse_pdf(pdf_path)

            # Step 2: Chunking
            chunks = chunk_markdown(
                markdown_content,
                source,
                CHUNK_SIZE,
                CHUNK_OVERLAP
            )

            # Step 3: Embedding
            embedded_vectors = embed(
                [c.page_content for c in chunks],
                BATCH_SIZE,
                self.model
            )

            # Step 4: Vector Storage
            add_chunks(chunks, embedded_vectors)

            return {
                "source": source,
                "total_chunks": len(chunks),
                "status": "success"
            }

        except Exception as e:
            raise CustomException(e, sys)
```

The pipeline separates processing logic from API implementation, allowing it to be reused by different application interfaces.

## 8. FastAPI Document Upload API

The document API receives PDF files from clients and invokes the indexing pipeline.

### Endpoint

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/documents/upload` | Upload and index a PDF document |

### Processing Flow

1. Validate the uploaded file extension.
2. Generate a unique filename using UUID.
3. Save the uploaded PDF into `RAW_DIR`.
4. Execute the indexing pipeline in a thread pool.
5. Return the indexing result to the client.

### Example Request

```bash
curl -X POST \
  "http://127.0.0.1:8000/api/v1/documents/upload" \
  -F "file=@bank_terms.pdf"
```

### Example Response

```json
{
    "message": "PDF indexed successfully",
    "filename": "bank_terms.pdf",
    "stored_filename": "uuid_bank_terms.pdf",
    "result": {
        "source": "uuid_bank_terms.pdf",
        "total_chunks": 25,
        "status": "success"
    }
}
```

## 9. Logging and Exception Handling

The project implements centralized logging to monitor application execution and identify processing errors.

### Logging

Logs are stored in the `logs/` directory with timestamp-based filenames.

The logging system records:

- Pipeline execution status.
- PDF parsing operations.
- Chunking results.
- Embedding execution.
- Vector database storage.
- Exceptions and stack traces.

### Exception Handling

A custom exception class is used to provide additional error context and traceback information.

This helps identify errors across different stages of the indexing pipeline.

## 10. Running the Application

### Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure `python-multipart` is installed for FastAPI file uploads.

```bash
pip install python-multipart
```

### Start FastAPI

Run the following command from the project root:

```bash
uvicorn src.main:app --reload
```

### Access Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Use the document upload endpoint to upload a PDF and test the indexing pipeline.

---

## 11. Current Development Status

**Completed / Implemented**

- [x] Project configuration and directory management.
- [x] PDF upload API structure.
- [x] PDF parsing module integration.
- [x] Markdown-based chunking pipeline.
- [x] Embedding generation integration.
- [x] ChromaDB persistent storage integration.
- [x] Indexing pipeline orchestration.
- [x] Logging and custom exception handling.

**Next Development Stages**

- [ ] Document retrieval using vector similarity search.
- [ ] Query embedding and top-k retrieval.
- [ ] LLM integration for answer generation.
- [ ] Context-aware responses with source citations.
- [ ] Chat API and conversational interface.
- [ ] Retrieval evaluation and performance optimization.
