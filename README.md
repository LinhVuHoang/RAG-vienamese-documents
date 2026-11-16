# Vietnamese Banking RAG

A Retrieval-Augmented Generation (RAG) application for querying Vietnamese banking documents using semantic search, Large Language Models (LLMs), and the Model Context Protocol (MCP).

The system provides a Streamlit frontend, FastAPI backend, and MCP server, supporting PDF ingestion, vector-based retrieval, context-aware question answering, and integration with MCP-compatible clients.

## 1. Overview

Vietnamese Banking RAG is a document question-answering system that allows users to upload banking PDF documents, index their contents, and ask questions based on the indexed information.

The project consists of three main components:

- **RAG Application:** Handles document ingestion, retrieval, and question answering.
- **Web Application:** Provides a Streamlit frontend and FastAPI backend.
- **MCP Server:** Exposes RAG capabilities through MCP Tools, Resources, and Prompts.

### Key Features

**Document Processing**
- Upload and index PDF documents.
- Extract and process PDF content into Markdown.
- Structure-aware text chunking using Markdown headings.
- Generate embeddings using Sentence Transformers.
- Persistent vector storage with ChromaDB.

**Retrieval and Generation**
- Semantic similarity search using cosine distance.
- Top-K document retrieval.
- Context-aware answer generation using Google Gemini.
- Source references with document names and page information.

**Web Application**
- Interactive chat interface built with Streamlit.
- PDF upload and indexing interface.
- Display retrieved source documents and page information.
- Session-level chat history.
- FastAPI REST API integration.

**MCP Integration**
- Expose document indexing and retrieval through MCP Tools.
- Provide document metadata through MCP Resources.
- Define reusable question-answering instructions through MCP Prompts.
- Support integration with MCP-compatible clients.
- Test MCP capabilities using MCP Inspector.

## 2. Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Backend API | FastAPI |
| API Validation | Pydantic |
| HTTP Client | Requests |
| Document Processing | PDF Parser |
| Text Chunking | LangChain Text Splitters |
| Embedding | Sentence Transformers |
| Vector Database | ChromaDB |
| Similarity Metric | Cosine Similarity |
| LLM | Google Gemini 3.1 Flash-Lite |
| LLM SDK | Google Gen AI SDK |
| MCP Framework | MCP Python SDK (FastMCP) |
| MCP Transport | STDIO |
| Configuration | python-dotenv |
| Logging | Python Logging |
| API Testing | FastAPI Swagger UI |
| MCP Testing | MCP Inspector |

## 3. System Architecture

The application follows a modular architecture consisting of the RAG processing layer, web application layer, and MCP integration layer.

### 3.1. Overall Architecture

```text
                         User
                           |
               +-----------+-----------+
               |                       |
               v                       v
        Streamlit Frontend       MCP-compatible Client
               |                       |
               v                       v
          FastAPI Backend           MCP Server
               |                       |
       +-------+-------+       +-------+-------+
       |               |       |       |       |
       v               v       v       v       v
  Indexing Pipeline  QA Pipeline Tools Resources Prompts
       |               |       |       |       |
       +-------+-------+       +-------+-------+
               |                       |
               v                       v
            ChromaDB              RAG Components
               |                       |
               +-----------+-----------+
                           |
                           v
                     Document Data
```

The web application and MCP server provide different interfaces to the underlying RAG capabilities.

- **Streamlit:** Provides the user-facing interface.
- **FastAPI:** Exposes REST endpoints for document ingestion and question answering.
- **MCP Server:** Exposes RAG functionality through the MCP protocol.
- **ChromaDB:** Stores document chunks and vector embeddings.

### 3.2. Indexing Pipeline

```text
PDF Upload
    |
    v
Streamlit Frontend / MCP Client
    |
    v
FastAPI Document API / MCP Tool
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
 Parsing    Chunking    Embedding
    |          |           |
    +----------+-----------+
               |
               v
           Store Layer
               |
               v
            ChromaDB
```

The indexing pipeline transforms PDF documents into searchable vector representations.

### 3.3. Retrieval and Generation Pipeline

```text
User Question
      |
      v
Streamlit / MCP Client
      |
      v
FastAPI Chat API / MCP Tool
      |
      v
Retrieval
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
```

The QA pipeline retrieves relevant document chunks and uses their contents as context for LLM generation.

### 3.4. MCP Architecture

The MCP server exposes three MCP primitives:

```text
                 MCP Client
                      |
                      v
               MCP Server
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
        Tools      Resources    Prompts
          |           |           |
          v           v           v
     RAG Actions  Document Data  Instructions
          |
    +-----+------+
    |            |
    v            v
 Indexing     Retrieval
 Pipeline     Pipeline
    |            |
    +------+-----+
           |
           v
        ChromaDB
```

**Tools**

Tools allow an MCP client to execute operations exposed by the server.

| Tool | Description |
|---|---|
| `greet` | Basic tool for testing MCP connectivity |
| `index_document` | Index a PDF document using the indexing pipeline |
| `search_documents` | Retrieve relevant document chunks from ChromaDB |

**Resources**

Resources provide data that MCP clients can discover and read.

| Resource URI | Description |
|---|---|
| `banking://documents` | Provides a list of available PDF documents and their metadata |

The Resource reads document information from the configured raw PDF directory.

**Prompts**

Prompts provide reusable instructions that MCP clients can retrieve and use.

| Prompt | Description |
|---|---|
| `answer_with_citations` | Provides instructions for answering Vietnamese banking questions using retrieved documents and source references |

The Prompt instructs the client to use `search_documents`, answer based on retrieved evidence, and include source citations.

> MCP Tools, Resources, and Prompts serve different purposes. Tools execute actions, Resources expose data, and Prompts provide reusable instructions. Their availability and interaction depend on the MCP client.

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
├── mcp_app/
│   ├── __init__.py
│   ├── server.py                    # MCP server initialization
│   ├── tools.py                     # MCP tool registration
│   ├── resources.py                 # MCP resource registration
│   └── prompts.py                   # MCP prompt registration
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

The project uses centralized configuration to manage storage paths and processing parameters.

Example:

```python

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

### 10.3. API Documentation

FastAPI automatically generates interactive API documentation.

After starting the backend, access:

```text
http://127.0.0.1:8000/docs
```

Use Swagger UI to test the upload and chat endpoints independently from the frontend.

## 11. MCP Server

The MCP server exposes selected RAG functionality through the Model Context Protocol.

It is implemented using the Python MCP SDK and FastMCP.

### 11.1. Server Initialization

The MCP server initializes the FastMCP instance and registers Tools, Resources, and Prompts.

The `IndexingPipeline` is initialized once and reused by the registered tools.

```python
from mcp.server.fastmcp import FastMCP
from src.Pipeline.Indexing_pipeline import IndexingPipeline

mcp = FastMCP("Vietnamese Document RAG")

indexing_pipeline = IndexingPipeline()
```

The server registers the components from separate modules:

```python
register_tools(mcp, indexing_pipeline)
register_resources(mcp)
register_prompts(mcp)
```

The server uses STDIO transport for local MCP client integration.

### 11.2. MCP Tools

Tools expose executable operations to MCP clients.

| Tool | Description |
|---|---|
| `greet` | Tests basic MCP server connectivity |
| `index_document` | Accepts a local PDF path and executes the indexing pipeline |
| `search_documents` | Performs semantic retrieval from the vector database |

**Indexing Tool**

The `index_document` tool accepts a PDF file path and invokes the existing indexing pipeline.

**Search Tool**

The `search_documents` tool accepts a query and retrieves relevant document chunks from ChromaDB.

The search tool focuses on retrieval and does not independently generate an LLM answer.

### 11.3. MCP Resources

Resources expose document-related information through a URI.

The project provides:

```text
banking://documents
```

This Resource returns a JSON-formatted list of PDF documents available in the configured raw document directory.

The returned metadata includes:

- File name.
- File size.
- File format.
- Total document count.

Resources allow compatible MCP clients to discover and read document information without executing an indexing operation.

### 11.4. MCP Prompts

The project provides the following reusable Prompt:

```text
answer_with_citations
```

It accepts:

| Argument | Description |
|---|---|
| `question` | User's banking-related question |
| `top_k` | Number of relevant document chunks to retrieve |

The Prompt provides instructions for an MCP client to:

1. Use `search_documents` to retrieve relevant document chunks.
2. Answer based only on retrieved evidence.
3. Include source references using document names and page numbers.
4. Avoid fabricated information and citations.
5. Explicitly state when the retrieved evidence is insufficient.
6. Respond in Vietnamese.

The Prompt provides instructions to the client; it does not independently execute retrieval or LLM generation.

### 11.5. MCP Transport

The server uses STDIO transport:

```python
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

STDIO allows a local MCP client to launch the server as a subprocess and communicate through standard input and output.

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

## 13. Running the Application Locally

### 13.1. Clone the Repository

```bash
git clone https://github.com/LinhVuHoang/RAG-vienamese-documents.git

cd RAG-vienamese-documents
```

### 13.2. Create a Virtual Environment

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

### 13.3. Install Dependencies

```bash
python -m pip install --upgrade pip

python -m pip install -r requirements.txt
```

```bash
python -m pip install "mcp[cli]>=1.28,<2"
```

### 13.4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

### 13.5. Start FastAPI Backend

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

### 13.6. Start Streamlit Frontend

Open a second terminal at the project root:

```bash
python -m streamlit run frontend/app.py
```

Streamlit runs at:

```text
http://localhost:8501
```

The frontend communicates with the local FastAPI backend through the configured `API_BASE_URL`.

### 13.7. Start MCP Server

The MCP server can be launched using the installed MCP SDK.

```bash
python -m mcp_app.server
```

Alternatively, use `uv` to run the server with the MCP dependency:

```bash
uv run --with "mcp[cli]>=1.28,<2" python -m mcp_app.server
```

The server communicates over STDIO and is intended to be launched by an MCP client rather than accessed through a browser URL.

### 