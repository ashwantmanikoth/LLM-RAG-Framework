
from typing import Optional, List
from openai import OpenAI
from utils.config import Config

openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)

def generate_embedding(prompt: str) -> Optional[List[float]]:
    """
    Generate an embedding for the given prompt using OpenAI.
    """
    try:
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=prompt,
        )
        return response.data[0].embedding

    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None
