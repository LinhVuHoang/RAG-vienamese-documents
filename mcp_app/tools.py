
import uuid
import shutil
from pathlib import Path

from src.Retrieval.retriever import retrieve
from src.config.config import RAW_DIR


def register_tools(mcp, indexing_pipeline):

    @mcp.tool()
    def greet(name: str) -> str:
        """
        Greet a user by name.
        """
        return f"Hello {name}! Welcome to MCP Server."


    @mcp.tool()
    def index_document(file_path: str) -> dict:
        """
        Index a PDF document into vector database.

        Args:
            file_path: Path to the PDF file.
        """

        source = Path(file_path).name
        pdf_path = None

        try:
            input_path = Path(file_path.strip().strip('"')).resolve()
            source = input_path.name

            # Validate input file
            if not input_path.is_file():
                raise FileNotFoundError(
                    f"File not found: {input_path}"
                )

            if input_path.suffix.lower() != ".pdf":
                raise ValueError("Only PDF files are supported")

            # Create unique filename
            RAW_DIR.mkdir(parents=True, exist_ok=True)

            stored_name = f"{uuid.uuid4().hex}_{source}"
            pdf_path = RAW_DIR / stored_name

            # Copy PDF into RAW_DIR
            shutil.copy2(input_path, pdf_path)

            # Run indexing pipeline
            result = indexing_pipeline.ingestion_pipeline(
                str(pdf_path)
            )

            if not result:
                raise RuntimeError("Document indexing failed")

            return {
                "status": "success",
                "file": source,
                "stored_name": stored_name,
                "message": result
            }

        except Exception as e:
            return {
                "status": "error",
                "file": source,
                "message": str(e)
            }


    @mcp.tool()
    def search_documents(query: str, top_k: int = 5) -> dict:
        """
        Search relevant chunks from the Vietnamese document database.

        Args:
            query: User's search query.
            top_k: Number of relevant chunks to retrieve.
        """

        results = retrieve(query, top_k)

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        retrieved_documents = []

        for document, metadata in zip(documents, metadatas):
            retrieved_documents.append({
                "content": document,
                "source": metadata.get("source", "Unknown"),
                "page": metadata.get("page", "Unknown")
            })

        return {
            "query": query,
            "results": retrieved_documents
        }
