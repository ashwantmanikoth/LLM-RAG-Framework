# my_app/main.py
from services.embedding_service import generate_embedding
from services.qdrant_service import search_qdrant
from services.llm_service import build_prompt, query_llm_ollama, query_llm_openai
from utils.formatters import (
    format_context,
)  # Assuming you have this from your original code.


def process_input(user_input: str, model: str, zip_code: str) -> str:
    """
    Orchestrates the entire flow:
    1. Generate embedding for user input.
    2. Search Qdrant for relevant chunks using zip_code filter.
    3. Format the returned context.
    4. Build a prompt and query the chosen LLM model.
    5. Return the final response.
    """
    # 1. Generate Embedding
    embedding = generate_embedding(user_input)
    if not embedding:
        return "Error generating embedding."

    # 2. Search Qdrant
    search_results = search_qdrant(embedding, zip_code=zip_code, top_k=20)
    if not search_results:
        return "No relevant information found. Please ask another question."

    # 3. Format context
    context = format_context(search_results)

    # 4. Build Prompt
    full_prompt = build_prompt(user_input, context)
    print("full_prompt", full_prompt)

    # 5. Query LLM
    if model.startswith("gpt-4o"):
        response = query_llm_openai(full_prompt, model)
    else:
        response = query_llm_ollama(full_prompt, model)

    return response
