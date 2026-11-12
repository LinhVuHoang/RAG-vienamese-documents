from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw" #Lưu tài liệu gốc
DB_DIR = ROOT / "data" / "vectordb" #Lưu vector database

EMBED_MODEL = "BAAI/bge-m3"
BATCH_SIZE = 8            # giữ nhỏ cho GTX 1650 4GB
MAX_SEQ_LENGTH = 512
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200
COLLECTION = "cv_chunks"