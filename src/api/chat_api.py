import os
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from src.Pipeline.QA_pipeline import QAPipeline
from starlette.concurrency import run_in_threadpool
from src.logger import logger


router = APIRouter()

pipeline = QAPipeline()

#Request schema
class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description = "User question"
    )
    
#Response schema

class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[dict]
    
@router.post("/chat", response_model=ChatResponse)
async def chat(request:ChatRequest):
    try:
        #Execute synchronous QA pipeline in threadpool
        result = await run_in_threadpool(
            pipeline.answer,
            request.question
        )
        
        return result
    except Exception as e:
        logger.exception("Failed to process chat request")
        
        
        raise HTTPException(
            status_code=500,
            detail="Failed to generate answer"
        ) from e