# my_app/llm_service.py
from ollama import chat
from typing import List
from utils.config import Config
from openai import OpenAI

openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)

def query_llm_ollama(prompt: str, model: str) -> str:
    response = chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.message.content

def query_llm_openai(prompt: str, model: str) -> str:
    """
    Query an OpenAI model with a prompt (example usage for GPT-4 or GPT-3).
    """
    response = openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content

def build_prompt(user_input: str, context: str) -> str:
    """
    Build the full prompt to pass to the LLM.
    """
    return (
        "You are a Medical Plan Advisor with access to a limited dataset of plans. "
        "Provide direct, informative answers in the form of lists based solely on the provided context. "
        "Avoid mentioning the context explicitly and ensure responses are complete and professional. "
        f"\nContext: {context}.\n"
        "If the context doesn't provide relevant information, respond with 'No relevant information found'."
        f"\nQuestion: {user_input}\n"
    )

