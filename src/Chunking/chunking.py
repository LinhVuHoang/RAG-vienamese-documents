#Bước 2 chunking (chia nhỏ tài liệu markdown thành các đoạn nhỏ, giữ ngữ cảnh)
from langchain_text_splitters import (
MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter)

def chunk_markdown(md: str, source: str,chunk_size: int =300, chunk_overlap: int = 100):
    headers = [("#", "h1"), ("##", "h2"), ("###", "h3")]
    sections = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers).split_text(md) #chia theo cấu trúc nội dung markdown, giữ nguyên header

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap)   # ~300 từ, overlap ~13% giữ ngữ cảnh
    chunks = splitter.split_documents(sections)

    for i, c in enumerate(chunks):
        c.metadata["source"] = source
        c.metadata["chunk_id"] = f"{source}-{i}"
    return chunks


