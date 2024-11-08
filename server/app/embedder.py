from dotenv import load_dotenv
import os

import google.generativeai as genai

class EmbedderManager:
    def __init__(self) -> None:
        self.__connectToLLM()


    def __connectToLLM(self):
        genai.configure(api_key = os.getenv("GG_GENAI_API_KEY"))
        print("[INFO] connected to LLM")

    def get_embedding(self, content):
        result = genai.embed_content(
            model = "models/embedding-001",
            content = content,
            task_type = "retrieval_document" 
            ) 
        return result['embedding']