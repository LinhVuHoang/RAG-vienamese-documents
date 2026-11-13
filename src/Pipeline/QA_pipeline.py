import os
import sys
from src.config.config import BATCH_SIZE
from src.Retrieval.retriever import retrieve
from src.Prompt.prompt_template import SYSTEM_PROMPT
from src.Generation.llm import generate
from src.logger import logger
from src.exception import CustomException
from src.config.config import TOP_K

class QAPipeline:
    def __init__(self):
        pass
        
    
    def answer(self, question:str):
        try:
            #B1: Retrieve
            logger.info("Retrieve Starting")
            results = retrieve(question,TOP_K)
            
            documents = results['documents'][0]
            metadatas = results['metadatas'][0]
            
            if not documents:
                return {
                "question": question,
                "answer": "Tôi không tìm thấy thông tin phù hợp trong tài liệu.",
                "sources": []
            }

            
            #B2 Build Context
            context_parts =[]
            logger.info("Building context")
            for document, metadata in zip(documents, metadatas):
                source = metadata.get("source","Unknown")
                page = metadata.get("page","Unknown")
                
                context_parts.append(
                    f"""
                    Source: {source}
                    Page: {page}
                    Content: {document}
                    
                    """
                    
                )
            
            context = "\n\n".join(context_parts)
            
            #B3 Build prompt
            
            logger.info("Building prompt")
            
            prompt = SYSTEM_PROMPT.format(
                context = context,
                question = question
            )
            #B4: generate answer
            logger.info("Answering...")
            response = generate(prompt)
            
            #B5: return Response
            logger.info("Answer successfuly!")
            return {
            "question": question,
            "answer": response,
            "sources": metadatas
        }
        except Exception as e:
            logger.error(f"Error: {e}")
            raise CustomException(e,sys)