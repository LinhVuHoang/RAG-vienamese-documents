import os
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.concurrency import run_in_threadpool
from src.config.config import RAW_DIR
from src.Pipeline.Indexing_pipeline import IndexingPipeline


#Chia API thành nhiều module riêng biệt, sau đó import và đăng ký chúng trong main.py
router = APIRouter()

#Khởi tạo pipeline một lần, tái sử dụng cho các request

pipeline = IndexingPipeline()

#Check Raw dir exists

RAW_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/documents/upload")

async def upload_pdf(file: UploadFile = File(...)):
    
    #Check input file
    
    
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
        

    #Create unique filename
    original_name = Path(file.filename).name
    stored_name = f"{uuid.uuid4().hex}_{original_name}"
    pdf_path = RAW_DIR/stored_name
    
    
    
    try:
        #Save PDF file into RAW_DIR
        with open(pdf_path,"wb") as f:
            while content := await file.read(1024 * 1024):
                f.write(content)

        #Call pipeline to process PDF file
        
        result = await run_in_threadpool(
            pipeline.ingestion_pipeline,
            str(pdf_path)
        )
        
        return {
            "message": result,
            "filename": original_name,
            "stored_filename": stored_name
        }
    except:
        raise HTTPException(
            status_code=500,
            detail="Failed to process PDF"
        )
    
    finally:
        await file.close()