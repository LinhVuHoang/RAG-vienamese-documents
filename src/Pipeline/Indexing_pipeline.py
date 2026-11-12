import os
import sys
from src.config.config import (DB_DIR, COLLECTION, BATCH_SIZE, CHUNK_SIZE, CHUNK_OVERLAP)
from src.Embedding.embedding import model, embed
from src.Parsing.parse_pdf import parse_pdf
from src.Chunking.chunking import chunk_markdown
from src.Store.store import add_chunks
from src.exception import CustomException
from src.logger import logger


class IndexingPipeline:
    def __init__(self):
        self.model = model
    
    def ingestion_pipeline(self, pdf_path: str):
        try:
            source = os.path.basename(pdf_path) #lấy tên file pdf làm source, ví dụ: "CV_HoangVuLinh.pdf", phục vụ cho metadata của chunk, giúp truy xuất nguồn gốc chunk khi tìm kiếm
            
            logger.info(f"Starting ingestion pipeline: {source}")
            
            #B1: Parsing (pdf --> markdown)
            
            logger.info(f"Starting PDF parsing")
            markdown_content = parse_pdf(pdf_path)    
            #B2: Chunking (markdown --> chunks)
            
            
            logger.info("Starting chunking")
            chunks = chunk_markdown(markdown_content, source, CHUNK_SIZE, CHUNK_OVERLAP)
            
            logger.info(f"Generated {len(chunks)} chunks")
            #B3: Embedding (chunks --> vectors)
            
            
            logger.info("Starting embedding")
            embedded_vectors = embed([c.page_content for c in chunks], BATCH_SIZE, self.model)
            
            #B4: Store (chunks + vectors --> vector database)
            logger.info("Starting storing database")
            add_chunks(chunks, embedded_vectors)
            
            logger.info("Done ingestion pipeline")
            
            return "PDF indexed successfully"
        except Exception as e:
            logger.error(f"Lỗi {e}")
            raise CustomException(e, sys)
        
        