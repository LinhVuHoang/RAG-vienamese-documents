#Bước 1 Parsing (pdf--> markdown)

import re, unicodedata
import pymupdf4llm

def parse_pdf(path: str) -> str:
    md = pymupdf4llm.to_markdown(path)
    md = unicodedata.normalize("NFC", md)   # chuẩn hóa dấu tiếng Việt
    md = re.sub(r"[ \t]+\n", "\n", md)      # bỏ khoảng trắng cuối dòng
    md = re.sub(r"\n{3,}", "\n\n", md)      # gộp dòng trống thừa
    return md

