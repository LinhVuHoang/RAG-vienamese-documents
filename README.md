# Vietnamese Banking RAG

A Retrieval-Augmented Generation (RAG) application for querying Vietnamese banking documents using semantic search and Large Language Models (LLMs). The system provides a Streamlit frontend and FastAPI backend, supporting PDF ingestion, vector-based retrieval, and context-aware question answering with source references.

## 1. Overview

Vietnamese Banking RAG is a document question-answering system that allows users to upload banking PDF documents, index their contents, and ask questions based on the indexed information.

The application follows a two-pipeline architecture:

- **Indexing Pipeline:** Parses PDF documents, extracts Markdown content, creates text chunks, generates embeddings, and stores them in ChromaDB.
- **QA Pipeline:** Embeds user queries, retrieves relevant document chunks, constructs prompts, and generates answers using Google Gemini.

### Key Features

- Upload and index PDF documents.
- Extract and process PDF content into Markdown.
- Structure-aware text chunking using Markdown headings.
- Generate text embeddings using Sentence Transformers.
- Persistent vector storage with ChromaDB.
- Semantic similarity search using cosine distance.
- Top-K document retrieval.
- Context-aware answer generation using Gemini.
- Display retrieved source documents and page information.
- Interactive chat interface built with Streamlit.
- Session-level chat history.
- Centralized logging and exception handling.

## 2. Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| HTTP Client | Requests |
| Backend API | FastAPI |
| API Validation | Pydantic |
| Document Processing | PDF Parser |
| Text Chunking | LangChain Text Splitters |
| Embedding | Sentence Transformers |
| Vector Database | ChromaDB |
| Similarity Metric | Cosine Similarity |
| LLM | Google Gemini 3.1 Flash-Lite |
| LLM SDK | Google Gen AI SDK |
| Configuration | python-dotenv |
| Logging | Python Logging |
| API Testing | FastAPI Swagger UI |

## 3. System Architecture

The application consists of three main components:

- **Streamlit:** Provides the user interface for document upload and question answering.
- **FastAPI:** Exposes REST APIs and orchestrates the processing pipelines.
- **ChromaDB:** Stores document chunks and their vector embeddings using persistent local storage.

### 3.1. Overall Architecture

```text
                       User
                         |
                         v
                 Streamlit Frontend
                         |
              +----------+----------+
              |                     |
          Upload PDF             Chat Query
              |                     |
              v                     v
         Document API             Chat API
              |                     |
              v                     v
       Indexing Pipeline         QA Pipeline
              |                     |
              v                     v
           ChromaDB <---------- Retrieval
                                    |
                                    v
                                  Gemini
                                    |
                                    v
                             Answer + Sources
                                    |
                                    v
                             Streamlit UI
```

### 3.2. Indexing Pipeline

```text
PDF Upload
    |
    v
Streamlit Frontend
    |
    v
FastAPI Document API
    |
    v
Save PDF to RAW_DIR
    |
    v
IndexingPipeline
    |
    +----------------------+
    |          |           |
    v          v           v
 Parsing   Chunking    Embedding
    |          |           |
    +----------+-----------+
               |
               v
           Store Layer
               |
               v
            ChromaDB
```

### 3.3. Retrieval and Generation Pipeline

```text
User Question
      |
      v
Streamlit Frontend
      |
      v
FastAPI Chat API
      |
      v
QAPipeline
      |
      v
Query Embedding
      |
      v
Similarity Search
      |
      v
Top-K Retrieval
      |
      v
Context Formatting
      |
      v
Prompt Construction
      |
      v
Gemini 3.1 Flash-Lite
      |
      v
Generated Answer + Sources
      |
      v
Streamlit Frontend
```

## 4. Project Structure

```text
Vietnamese-Banking-RAG/
│
├── data/
│   ├── raw/                         # Uploaded PDF documents
│   └── vectordb/                    # Persistent ChromaDB storage
│
├── logs/                            # Application logs
│
├── frontend/
│   └── app.py                       # Streamlit application
│
├── src/
│   ├── api/
│   │   ├── document_api.py          # PDF upload endpoint
│   │   └── chat_api.py              # Chat endpoint
│   │
│   ├── config/
│   │   └── config.py                # Centralized configuration
│   │
│   ├── Parsing/
│   │   └── parse_pdf.py             # PDF parsing
│   │
│   ├── Chunking/
│   │   └── chunking.py              # Markdown text chunking
│   │
│   ├── Embedding/
│   │   └── embedding.py             # Embedding model and inference
│   │
│   ├── Store/
│   │   └── store.py                 # ChromaDB operations
│   │
│   ├── Retrieval/
│   │   └── retriever.py             # Query embedding and retrieval
│   │
│   ├── Prompt/
│   │   └── prompt_template.py       # LLM prompt template
│   │
│   ├── Generation/
│   │   └── llm.py                   # Gemini integration
│   │
│   ├── Pipeline/
│   │   ├── Indexing_pipeline.py     # Document indexing pipeline
│   │   └── QA_pipeline.py           # Retrieval and generation pipeline
│   │
│   ├── logger.py                    # Logging configuration
│   ├── exception.py                 # Custom exception handling
│   └── main.py                      # FastAPI application
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── pyproject.toml
└── README.md
```

## 5. Configuration

The project uses a centralized configuration file to manage storage paths and processing parameters.

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
| `RAW_DIR` | Directory for uploaded PDF documents |
| `DB_DIR` | Persistent ChromaDB storage directory |
| `COLLECTION` | ChromaDB collection name |
| `BATCH_SIZE` | Number of texts processed per embedding batch |
| `CHUNK_SIZE` | Target chunk size |
| `CHUNK_OVERLAP` | Overlapping characters between chunks |

### Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

The `.env.example` file can be used as a template:

```env
GEMINI_API_KEY=
```

**Important:** Never commit your actual `.env` file or expose API credentials in source code or public repositories.

## 6. Document Ingestion Pipeline

The indexing pipeline transforms raw PDF documents into searchable vector representations.

### 6.1. PDF Parsing

**Input:** PDF file path.

**Output:** Extracted Markdown or text content.

```python
markdown_content = parse_pdf(pdf_path)
```

The parsing module extracts textual content from PDF documents and prepares it for downstream processing. Markdown representation helps preserve document structure when available.

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

- `page_content`: Extracted text content.
- `metadata`: Source document, chunk ID, page information when available, and heading information.

### 6.3. Embedding Generation

**Input:** List of text chunks.

**Output:** List of numerical vectors.

The embedding module uses a Sentence Transformer model to convert text into vector representations.

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

- Batch processing for efficient embedding generation.
- Normalized embeddings for cosine similarity-based retrieval.
- Python list conversion for compatibility with ChromaDB.

The same embedding model is reused in both indexing and retrieval to ensure consistent vector representations.

### 6.4. Vector Storage

**Input:** Document chunks and their embeddings.

**Output:** Data stored in ChromaDB.

ChromaDB uses persistent local storage:

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
| Metadatas | Source and document metadata |

Persistent storage allows indexed data to remain available after restarting the application.

## 7. Retrieval Pipeline

The retrieval pipeline searches for document chunks relevant to a user's question.

### 7.1. Query Embedding

**Input:** User query.

**Output:** Query embedding vector.

The same embedding model used during indexing converts the user query into a vector.

```python
query_vector = embed(
    texts=[query],
    batch_size=1,
    model=model
)[0]
```

Using the same model ensures that query vectors and document vectors share the same embedding space.

### 7.2. Similarity Search and Top-K Retrieval

**Input:** Query embedding vector.

**Output:** Top-K relevant document chunks.

The storage module performs similarity search using ChromaDB:

```python
def search(query_vec, k=5):
    return collection.query(
        query_embeddings=[query_vec],
        n_results=k
    )
```

The retrieval module combines query embedding and vector search:

```python
def retrieve(query: str, top_k: int = 5):
    query_vector = embed(
        texts=[query],
        batch_size=1,
        model=model
    )[0]

    results = search(query_vector, k=top_k)

    return results
```

Retrieved results contain:

- `documents`: Retrieved document contents.
- `metadatas`: Associated document metadata.
- `distances`: Similarity search distances.
- `ids`: Retrieved chunk identifiers.

The Top-K results are passed to the QA pipeline for context construction.

## 8. Prompt Engineering and LLM Generation

This stage combines the user query and retrieved document context to generate a context-aware answer.

### 8.1. Prompt Template

The prompt template defines the instructions and context provided to the LLM.

The system prompt is designed for Vietnamese banking question answering.

Main instructions include:

- Answer using information from the retrieved context.
- Do not invent or assume information not present in the context.
- Indicate when the retrieved context does not contain sufficient information.
- Respond in Vietnamese.
- Include references to the source document and page when available.

Example prompt structure:

```text
You are an AI assistant specializing in Vietnamese banking information.

Instructions:
1. Answer using only the provided context.
2. Do not invent or assume missing information.
3. If the context does not contain the answer, state that
   the information cannot be found in the provided documents.
4. Answer clearly in Vietnamese.
5. Reference the source document and page when available.

CONTEXT:
{context}

USER QUESTION:
{question}
```

### 8.2. Gemini Integration

The Generation module integrates Google Gemini through the Google Gen AI SDK.

```python
from google import genai
import os

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL_NAME = "gemini-3.1-flash-lite"

def generate(prompt: str):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text
```

The generation module receives the constructed prompt and returns the LLM-generated response.

## 9. QA Pipeline Implementation

The `QAPipeline` class orchestrates retrieval, context formatting, prompt construction, and LLM generation.

### Processing Flow

1. Receive a user question.
2. Retrieve relevant document chunks.
3. Extract documents and metadata.
4. Format retrieved chunks into context.
5. Construct the prompt using the question and retrieved context.
6. Send the prompt to Gemini.
7. Return the generated answer and source metadata.

The QA pipeline provides a unified interface for the complete retrieval and generation process.

## 10. FastAPI Backend

The application exposes REST APIs for document ingestion and question answering.

### 10.1. Document Upload API

**Endpoint:**

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/documents/upload` | Upload and index a PDF document |

**Processing Flow:**

1. Validate the uploaded file extension.
2. Generate a unique filename using UUID.
3. Save the uploaded PDF into `RAW_DIR`.
4. Execute the indexing pipeline in a thread pool.
5. Return the indexing result to the client.

**Example Request:**

```bash
curl -X POST \
  "http://127.0.0.1:8000/api/v1/documents/upload" \
  -F "file=@bank_terms.pdf"
```

### 10.2. Chat API

**Endpoint:**

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/chat` | Ask questions about indexed banking documents |

The Chat API receives user questions and invokes the QA pipeline.

**Example Request:**

```json
{
    "question": "What are the requirements for opening a credit card?"
}
```

**Example Response:**

```json
{
    "question": "What are the requirements for opening a credit card?",
    "answer": "According to the retrieved banking document...",
    "sources": [
        {
            "source": "bank_terms.pdf",
            "page": 5,
            "chunk_id": "bank_terms.pdf-0"
        }
    ]
}
```

The response structure contains:

| Field | Description |
|---|---|
| `question` | Original user question |
| `answer` | LLM-generated answer |
| `sources` | Metadata of retrieved document chunks |

The Chat API uses `run_in_threadpool()` to execute the synchronous QA pipeline without blocking FastAPI's event loop.

### 10.3. API Documentation

FastAPI automatically generates interactive API documentation.

After starting the backend, access:

```text
http://127.0.0.1:8000/docs
```

Use Swagger UI to test the upload and chat endpoints independently from the frontend.

## 11. Streamlit Frontend

The frontend is built with Streamlit and communicates with FastAPI through HTTP requests.

### 11.1. Frontend Features

- PDF document upload.
- Trigger document indexing through the Document Upload API.
- Interactive chat interface.
- Display user questions and generated answers.
- Display retrieved source information, including document name and page when available.
- Maintain chat history using Streamlit Session State during the current session.
- Clear chat history through the sidebar.

### 11.2. Frontend and Backend Integration

The Streamlit application communicates with the following endpoints:

| Feature | HTTP Method | API Endpoint |
|---|---|---|
| Upload and index PDF | POST | `/api/v1/documents/upload` |
| Ask a question | POST | `/api/v1/chat` |

The frontend sends PDF files using multipart form data and sends chat questions as JSON.

Example chat request:

```python
response = requests.post(
    CHAT_URL,
    json={"question": question},
    timeout=120
)

response.raise_for_status()
result = response.json()

answer = result.get("answer", "No answer returned.")
sources = result.get("sources", [])
```
## 12. Running the Application Locally

### 12.1. Clone the Repository

```bash
git clone https://github.com/LinhVuHoang/RAG-vienamese-documents.git

cd RAG-vienamese-documents
```

### 12.2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv

.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 12.3. Install Dependencies

```bash
python -m pip install --upgrade pip

python -m pip install -r requirements.txt
```

Ensure the required dependencies are included in `requirements.txt`, such as:

- FastAPI
- Uvicorn
- python-multipart
- sentence-transformers
- chromadb
- google-genai
- python-dotenv
- Streamlit
- Requests
- langchain-text-splitters

### 12.4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

### 12.5. Start FastAPI Backend

Open the first terminal at the project root:

```bash
python -m uvicorn src.main:app --reload
```

FastAPI runs at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

### 12.6. Start Streamlit Frontend

Open a second terminal at the project root:

```bash
python -m streamlit run frontend/app.py
```

Streamlit runs at:

```text
http://localhost:8501
```

The frontend communicates with the local FastAPI backend through the configured `API_BASE_URL`.

## 13. Deployment Architecture

The application can be demonstrated remotely using Streamlit Community Cloud while keeping the FastAPI backend and ChromaDB on a local machine.

### 13.1. Demo Deployment Architecture

```text
                  Remote User
                       |
                       v
             Streamlit Community Cloud
                       |
                       | HTTPS Request
                       v
              Cloudflare Quick Tunnel
                       |
                       v
                Local FastAPI
                       |
             +---------+---------+
             |                   |
             v                   v
         QA Pipeline       Indexing Pipeline
             |                   |
             v                   v
           Gemini              ChromaDB
                                 |
                                 v
                         Local Persistent Disk
```

### 13.2. Deployment Components

| Component | Hosting / Storage |
|---|---|
| Streamlit Frontend | Streamlit Community Cloud |
| FastAPI Backend | Local machine |
| Public API Access | Cloudflare Quick Tunnel |
| Vector Database | Local persistent ChromaDB |
| LLM | Google Gemini API |

### 13.3. API Configuration

For local development, the frontend can use:

```python
API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)
```

For Streamlit Community Cloud, configure `API_BASE_URL` through Streamlit Secrets:

```toml
API_BASE_URL = "https://your-tunnel-url.trycloudflare.com"
```

The Cloudflare Quick Tunnel URL exposes the local FastAPI service to the Streamlit Cloud application.

**Deployment limitations:**

- The local machine must remain powered on and connected to the Internet.
- FastAPI and Cloudflare Tunnel must remain running.
- The Quick Tunnel URL may change when the tunnel is recreated.
- ChromaDB remains stored on the local machine.
- This setup is intended for demonstration and testing, not reliable production hosting.

The backend and vector database are not hosted on AWS in this deployment architecture.

## 14. Security Considerations

When exposing the backend through a public tunnel, consider the following:

- Keep the Gemini API key in environment variables or Streamlit Secrets.
- Never commit `.env` or other credential files.
- Protect public API endpoints with authentication before sharing the application.
- Validate uploaded files and restrict file sizes.
- Avoid exposing internal exception details through API responses.
- Restrict access to document upload endpoints to prevent unauthorized indexing.

## 15. Development Status

### Completed

- [x] Project configuration and directory management.
- [x] PDF upload API.
- [x] PDF parsing module integration.
- [x] Markdown-based chunking pipeline.
- [x] Embedding generation integration.
- [x] ChromaDB persistent storage integration.
- [x] Indexing pipeline orchestration.
- [x] Query embedding.
- [x] Vector similarity search.
- [x] Top-K document retrieval.
- [x] Prompt template construction.
- [x] Gemini LLM integration.
- [x] Context-aware answer generation.
- [x] QA pipeline orchestration.
- [x] Chat API implementation.
- [x] Logging and custom exception handling.
- [x] Streamlit frontend implementation.
- [x] PDF upload interface.
- [x] Chat interface and answer display.
- [x] Retrieved source display.
- [x] Session-level chat history.

### Potential Future Improvements

- [ ] Retrieval quality evaluation.
- [ ] Similarity score thresholding.
- [ ] Reranking retrieved chunks.
- [ ] Improved citation generation and validation.
- [ ] Persistent conversation history and multi-turn chat.
- [ ] Streaming LLM responses.
- [ ] Improved document management interface.
- [ ] API authentication and rate limiting.
- [ ] Dockerization.
- [ ] Stable cloud deployment.
- [ ] Performance optimization and monitoring.

## 16. Future Development Direction

Potential next steps for improving the project include:

1. **Retrieval Evaluation:** Build a test dataset to evaluate retrieval relevance and answer quality.
2. **Retrieval Optimization:** Experiment with similarity thresholds and reranking strategies.
3. **Answer Reliability:** Improve source attribution and validate generated citations.
4. **Deployment:** Move the backend and vector database to a stable hosting environment.
5. **Production Readiness:** Introduce authentication, request limits, monitoring, and persistent conversation storage.