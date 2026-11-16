from src.config.config import RAW_DIR

for pdf_file in sorted(RAW_DIR.glob("*.pdf")):
            
     print(f"File_name: {pdf_file.name.split(pdf_file.name.split("_")[0])[1].strip("_")}")
     print(f"Size: {pdf_file.stat().st_size}")
     
     print("_____________________________________")