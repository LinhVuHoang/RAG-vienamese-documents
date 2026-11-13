# # #Bước 1 Parsing (pdf--> markdown)

# # import re, unicodedata
# # import pymupdf4llm

# # def parse_pdf(path: str) -> str:
# #     md = pymupdf4llm.to_markdown(path)
# #     md = unicodedata.normalize("NFC", md)   # chuẩn hóa dấu tiếng Việt
# #     md = re.sub(r"[ \t]+\n", "\n", md)      # bỏ khoảng trắng cuối dòng
# #     md = re.sub(r"\n{3,}", "\n\n", md)      # gộp dòng trống thừa
# #     return md


# # # print(parse_pdf(r"C:\Users\HLC_2021\Downloads\CV_HoangVuLinh.pdf")) #khai báo rawstring, không xử lý các \
    
# # #Bước 2 chunking (chia nhỏ tài liệu markdown thành các đoạn nhỏ, giữ ngữ cảnh)
# # from langchain_text_splitters import (
# # MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter)

# # def chunk_markdown(md: str, source: str):
# #     headers = [("#", "h1"), ("##", "h2"), ("###", "h3")]
# #     sections = MarkdownHeaderTextSplitter(
# #         headers_to_split_on=headers).split_text(md) #chia theo cấu trúc nội dung markdown, giữ nguyên header

# #     splitter = RecursiveCharacterTextSplitter(
# #         chunk_size=300, chunk_overlap=100)   # ~300 từ, overlap ~13% giữ ngữ cảnh
# #     chunks = splitter.split_documents(sections)

# #     for i, c in enumerate(chunks):
# #         c.metadata["source"] = source
# #         c.metadata["chunk_id"] = f"{source}-{i}"
# #     return chunks

# # chunks_list =chunk_markdown(parse_pdf(r"C:\Users\HLC_2021\Downloads\CV_HoangVuLinh.pdf"), "CV_HoangVuLinh.pdf")

# # # for i, c in enumerate(chunks_list):

# # #     print(f"Chunk {i}: {c.metadata}")
# # #     print(f"Length: {len(c.page_content)} characters")
# # #     print(c.page_content)
# # #     print("--------------------------------------------------")

# # #Bước 3: embedding (chuyển các đoạn nhỏ thành vector để lưu trữ và truy vấn)

# # from sentence_transformers import SentenceTransformer

# # model = SentenceTransformer("BAAI/bge-m3")
# # def embed(texts: list[str]):
# #     return model.encode(
# #         texts, batch_size=16,
# #         normalize_embeddings=True,   # cần cho cosine similarity, chuẩn hóa vector embedding về độ dài (L2 norm) =1 vd: vector được chuẩn hóa về [0.6,0.8] --> tính độ dài bằng công thức L2 norm = sqrt(0.6^2 + 0.8^2) = 1, giúp tính cosine similarity chính xác hơn
# #         show_progress_bar=True,
# #     ).tolist() #chuyển numpy array thành python list để lưu trữ vào vector database
    
# # # print(embed([c.page_content for c in chunks_list]))

# import chromadb

# client = chromadb.PersistentClient(
#     path="./chroma_db"
# )

# print("ChromaDB installed successfully!")

from src.Pipeline.QA_pipeline import QAPipeline

qa = QAPipeline()

question = "chấm dứt phong tỏa tài khoản khi nào?"

result = qa.answer(question)

print("Question:", result["question"])
print("Answer:", result["answer"])
print("Sources:")

for source in result["sources"]:
    print(source)