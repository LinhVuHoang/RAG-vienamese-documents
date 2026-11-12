#Bước 3: embedding (chuyển các đoạn nhỏ thành vector để lưu trữ và truy vấn)

from sentence_transformers import SentenceTransformer
from src.config.config import EMBED_MODEL, MAX_SEQ_LENGTH
import torch



model = SentenceTransformer(EMBED_MODEL, device="cuda" if torch.cuda.is_available() else "cpu")
model.max_seq_length = MAX_SEQ_LENGTH  # giới hạn độ dài chuỗi đầu vào để tránh lỗi GPU out of memory
def embed(texts: list[str], batch_size: int, model: SentenceTransformer = model):
    return model.encode(
        texts, batch_size=batch_size,
        normalize_embeddings=True,   # cần cho cosine similarity, chuẩn hóa vector embedding về độ dài (L2 norm) =1 vd: vector được chuẩn hóa về [0.6,0.8] --> tính độ dài bằng công thức L2 norm = sqrt(0.6^2 + 0.8^2) = 1, giúp tính cosine similarity chính xác hơn
        show_progress_bar=True,
    ).tolist() #chuyển numpy array thành python list để lưu trữ vào vector database

