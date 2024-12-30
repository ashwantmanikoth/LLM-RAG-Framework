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
        "You are a highly knowledgeable Medical Plan Advisor. Your role is to assist users by explaining plan details, medical benefits, costs, and providing comparisons between multiple plans when applicable. You offer concise, accurate, and easy-to-understand answers"
        "Focus strictly on the information provided in the given context."
        "Present your responses in well-organized heading and paragraph format. If comparing multiple plans start with the cost difference."
        "With a maximum of 300 words per response."
        f"\nDo not mention the term 'context' or explain the limitations of the provided information."
        "Ignore case sensitivity and punctuation of the context."
        f"\n {context}.\n"
        # "If the context has any details that can answer the Question logically else say 'No Information found' ."
        f"\nQuestion: {user_input}\n"
    )

