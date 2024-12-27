# my_app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPEN_API_KEY", "")
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    COLLECTION_NAME = "medical_plan_embeddings_v10_chunks_company"
