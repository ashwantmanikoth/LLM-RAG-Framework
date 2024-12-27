from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
from utils.formatters import format_context
from ollama import chat
from ollama import ChatResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


QDRANT_CLIENT = QdrantClient("http://localhost:6333")

COLLECTION_NAME = "medical_plan_embeddings_v10_chunks_company"

openai_client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))


def generate_embedding(prompt: str, zip_code: str) -> Optional[List[float]]:
    """Generate an embedding for the prompt."""
    try:
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=f"{prompt}",
        )

        return response.data[0].embedding

    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None


def search_qdrant(
    query_embedding: List[float], zip_code: str, top_k: int = 10
) -> List[dict]:
    """Search Qdrant for relevant results."""
    try:

        results = QDRANT_CLIENT.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            query_filter=Filter(
                must=[FieldCondition(key="Zip_code", match=MatchValue(value=zip_code))]
            ),
            score_threshold = 0.75,
            limit=top_k,
            with_payload=True,
        )

        
        print(f"Qdrant search results: {results}")
        return results

    except Exception as e:
        print(f"Error during Qdrant search: {e}")
        return []


def query_llm(prompt: str, context: str, model: str) -> str:
    """Query LLM with formatted context."""

    full_prompt = (
        "You are a Medical Plan Advisor with access to a limited dataset of plans. "
        "Provide direct, informative answers in the form of lists based solely on the provided context. "
        "Avoid mentioning the context explicitly and ensure responses are complete and professional. "
        "\nContext:{context}.\n"
        "If the context doesn't provide relevant information, respond with 'No relevant information found'."
        f"\nQuestion: {prompt}\n"
    )

    if model == "gpt-4o":
        response = openai_client.chat.completions.create(
            model="gpt-4o", messages=[{"role": "user", "content": context}],
            temperature=0.5
        )

        return response.choices[0].message.content

    else:
        response = chat(
            model=model, messages=[{"role": "user", "content": full_prompt}]
        )

        return response.message.content


def process_input(user_input: str, model: str, zip_code: str) -> str:
    """Process user input and generate response."""

    embedding = generate_embedding(user_input, zip_code)

    if not embedding:
        return "Error generating embedding."

    search_results = search_qdrant(embedding, zip_code)
    if search_results==[]:
        return "No relevant information found. Please ask another question."
    
    context = format_context(search_results)

    return query_llm(user_input, context, model)
