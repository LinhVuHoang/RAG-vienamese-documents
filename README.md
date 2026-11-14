# Vietnamese Banking RAG

A Retrieval-Augmented Generation (RAG) application for querying Vietnamese banking documents using semantic search and Large Language Models (LLMs), with a Streamlit frontend and FastAPI backend.

## 1. Overview

Vietnamese Banking RAG is a document question-answering system that allows users to upload banking PDF documents, process and index their content, and ask questions based on the indexed information through a chat interface.

The system uses a two-pipeline architecture:

- **Indexing Pipeline:** Processes PDF documents, extracts content, creates text chunks, generates embeddings, and stores them in ChromaDB.
- **QA Pipeline:** Embeds user queries, retrieves relevant document chunks, constructs prompts, and generates answers using Gemini.

A Streamlit frontend provides document upload and an interactive chat interface, while FastAPI handles the backend processing.

### Current Scope

- PDF document upload through Streamlit and REST API.
- PDF parsing and Markdown extraction.
- Structure-aware text chunking.
- Text embedding generation.
- Persistent vector storage using ChromaDB.
- Semantic similarity search.
- Top-K document retrieval.
- Prompt construction with retrieved context.
- LLM integration using Gemini 3.1 Flash-Lite.
- Context-aware answer generation.
- Chat API for question answering.
- Interactive Streamlit chat interface.
- Retrieved source display.
- Chat history within the current Streamlit session.
- Logging and exception handling.

## 2. Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Frontend HTTP Client | Requests |
| Backend API | FastAPI |
| API Validation | Pydantic |
| Document Processing | PDF Parser |
| Text Chunking | LangChain Text Splitters |
| Embedding | Sentence Transformers |
| Vector Database | ChromaDB |
| Similarity Metric | Cosine Similarity |
| LLM | Google Gemini 3.1 Flash-Lite |
| LLM SDK | Google Gen AI SDK |
| Environment Variables | python-dotenv |
| Logging | Python Logging |
| API Testing | FastAPI Swagger UI |

## 3. System Architecture

The application consists of a Streamlit frontend, FastAPI backend, and two main processing pipelines.

### 3.1. Overall Application Architecture

```text
                 User
                  |
                  v
           Streamlit Frontend
                  |
          +-------+-------+
          |               |
      Upload PDF       Chat Query
          |               |
          v               v
     Document API      Chat API
          |               |
          v               v
    Indexing Pipeline   QA Pipeline
          |               |
          v               v
       ChromaDB <---- Retrieval
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
                  Client
                    |
                    | Upload PDF
                    v
              Streamlit UI
                    |
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
          +---------+---------+
                    |
                    v
                Store Layer
                    |
                    v
                  ChromaDB
```

### 3.3. Retrieval & Generation Pipeline

```text
                  User
                    |
                    | User Query
                    v
              Streamlit UI
                    |
                    v
                 Chat API
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
               Prompt Template
                    |
                    v
             Gemini 3.1 Flash-Lite
                    |
                    v
               Generated Answer
                    |
                    v
               Answer + Sources
                    |
                    v
              Streamlit UI
```

## 4. Project Structure

```text
Vietnamese-Banking-RAG/
│
├── data/
│   ├── raw/                       # Original uploaded PDF files
│   └── vectordb/                  # Persistent ChromaDB storage
│
├── logs/                          # Application logs
│
├── frontend/
│   └── app.py                     # Streamlit application
│
├── src/
│   ├── api/
│   │   ├── document_api.py        # PDF upload endpoint
│   │   └── chat_api.py            # Chat endpoint
│   │
│   ├── config/
│   │   └── config.py              # Project configuration
│   │
│   ├── Parsing/
│   │   └── parse_pdf.py           # PDF parsing
│   │
│   ├── Chunking/
│   │   └── chunking.py            # Markdown chunking
│   │
│   ├── Embedding/
│   │   └── embedding.py           # Embedding model and inference
│   │
│   ├── Store/
│   │   └── store.py               # ChromaDB operations
│   │
│   ├── Retrieval/
│   │   └── retriever.py           # Query embedding and retrieval
│   │
│   ├── Prompt/
│   │   └── prompt_template.py     # LLM prompt template
│   │
│   ├── Generation/
│   │   └── llm.py                 # Gemini integration
│   │
│   ├── Pipeline/
│   │   ├── Indexing_pipeline.py   # Document indexing pipeline
│   │   └── QA_pipeline.py         # Retrieval and generation pipeline
│   │
│   ├── logger.py                  # Logging configuration
│   ├── exception.py               # Custom exception handling
│   └── main.py                    # FastAPI application
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── pyproject.toml
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

### Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

A `.env.example` file can be provided as a configuration template:

```env
GEMINI_API_KEY=
```

Do not commit the actual `.env` file or expose API credentials in source code.

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

### 6.3. Embedding Generation

**Input:** List of text chunks.

**Output:** List of numerical vectors.

The embedding module converts textual chunks into vector representations using a Sentence Transformer model.

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

The same embedding model is reused in both the indexing and retrieval pipelines to ensure consistent vector representations.

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

## 8. Retrieval Pipeline

The retrieval pipeline searches for document chunks relevant to a user's question.

It consists of two main stages.

### 8.1. Query Embedding

**Input:** User query.

**Output:** Query embedding vector.

The same embedding function and model used during indexing are reused to convert the user query into a vector.

```python
query_vector = embed(
    texts=[query],
    batch_size=1,
    model=model
)[0]
```

Using the same embedding model ensures that query vectors and document vectors share the same embedding space.

### 8.2. Similarity Search and Top-K Retrieval

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

The retrieved results contain:

- `documents`: Retrieved document contents.
- `metadatas`: Associated document metadata.
- `distances`: Similarity search distances.
- `ids`: Retrieved chunk identifiers.

The Top-K results are passed to the QA pipeline for context construction.

## 9. Prompt Engineering and LLM Generation

This stage combines the user query and retrieved document context to generate a context-aware answer.

### 9.1. Prompt Template

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

### 9.2. Gemini Integration

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

## 10. QA Pipeline Implementation

The `QAPipeline` class orchestrates retrieval, context formatting, prompt construction, and LLM generation.

### Processing Flow

1. Receive a user question.
2. Retrieve relevant document chunks.
3. Extract documents and metadata.
4. Format retrieved chunks into context.
5. Construct the prompt using the question and context.
6. Send the prompt to Gemini.
7. Return the generated answer and source metadata.

The QA pipeline provides a unified interface for the complete retrieval and generation process.

## 11. FastAPI APIs

The application exposes REST APIs for document ingestion and question answering.

### 11.1. Document Upload API

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

### 11.2. Chat API

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

## 12. Streamlit Frontend

The frontend is built with Streamlit and communicates with FastAPI through HTTP requests.

### 12.1. Frontend Features

- PDF document upload.
- Trigger document indexing through the Document Upload API.
- Interactive chat interface.
- Display user questions and generated answers.
- Display retrieved source information, including document name and page when available.
- Maintain chat history using Streamlit Session State during the current session.
- Clear chat history through the sidebar.

### 12.2. Frontend and Backend Integration

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

### 12.3. Chat History

Streamlit Session State stores the messages during the current session.

```python
if "messages" not in st.session_state:
    st.session_state.messages = []
```

Each message is stored with its role and content. Assistant messages also contain retrieved source metadata.

```python
st.session_state.messages.append({
    "role": "assistant",
    "content": answer,
    "sources": sources
})
```

The chat history is rendered on subsequent Streamlit reruns. This implementation maintains session-level history; persistent conversation storage across sessions is a potential future improvement.

## 13. Logging and Exception Handling

The project implements centralized logging to monitor application execution and identify processing errors.

### Logging

Logs are stored in the `logs/` directory with timestamp-based filenames.

The logging system records:

- Pipeline execution status.
- PDF parsing operations.
- Chunking results.
- Embedding execution.
- Vector database storage.
- Retrieval and generation errors.
- Exceptions and stack traces.

### Exception Handling

A custom exception class is used to provide additional error context and traceback information.

API endpoints also handle exceptions and return appropriate HTTP error responses without exposing internal error details to clients.

## 14. Running the Application

### 14.1. Install Dependencies

Run from the project root:

```bash
python -m pip install -r requirements.txt
```

Make sure the required dependencies are installed, including:

- FastAPI
- Uvicorn
- python-multipart
- sentence-transformers
- chromadb
- google-genai
- python-dotenv
- Streamlit
- Requests

If Streamlit and Requests are not included in `requirements.txt`, install them separately:

```bash
python -m pip install streamlit requests
```

### 14.2. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

### 14.3. Start FastAPI Backend

Open the first terminal at the project root:

```bash
python -m uvicorn src.main:app --reload
```

FastAPI runs at:

```text
http://127.0.0.1:8000
```

### 14.4. Start Streamlit Frontend

Open a second terminal at the project root:

```bash
python -m streamlit run frontend/app.py
```

Streamlit runs at:

```text
http://localhost:8501
```

### 14.5. Access Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Use Swagger UI to test the backend APIs independently from the frontend.

## 15. Current Development Status

### Completed / Implemented

- [x] Project configuration and directory management.
- [x] PDF upload API structure.
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
- [ ] Dockerization.
- [ ] AWS deployment.
- [ ] Performance optimization and monitoring.

---

## 16. End-to-End Workflow

The complete application workflow consists of two main processes.

**Document Indexing:**

```text
PDF Upload
    → Streamlit Frontend
    → FastAPI Document API
    → PDF Parsing
    → Text Chunking
    → Embedding Generation
    → ChromaDB Storage
```

**Question Answering:**

```text
User Query
    → Streamlit Frontend
    → FastAPI Chat API
    → Query Embedding
    → Similarity Search
    → Top-K Retrieval
    → Context Formatting
    → Prompt Construction
    → Gemini Generation
    → Answer + Sources
    → Streamlit Frontend
```

The two pipelines work together to provide a document-grounded question-answering system for Vietnamese banking information.