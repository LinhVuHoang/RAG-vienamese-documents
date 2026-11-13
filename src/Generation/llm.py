from google import genai
import os
from dotenv import load_dotenv
from src.logger import logger
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY is not configured")
    raise ValueError("GEMINI_API_KEY is not configured")


client = genai.Client(
    api_key=os.getenv(GEMINI_API_KEY)
)
MODEL_NAME = "gemini-3.1-flash-lite"

def generate(prompt: str):
    response = client.models.generate_content(
        model = MODEL_NAME,
        contents = prompt
    )
    
    return response.text



# response = generate("Xin chào, hãy giới thiệu ngắn gọn về bạn.")
# print(response)