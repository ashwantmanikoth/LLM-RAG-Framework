from typing import List

def format_context(search_results: List[dict], max_length: int = 10000) -> str:
    """Format Qdrant search results for context."""
    context = ""
    
    for result in search_results:
        payload = result.payload
        field = payload.get("Field", "Unknown Field")
        plan_id = payload.get("Plan ID", "Unknown Plan ID")
        text = payload.get("Full Text", "No text available")
        context += f"- {field}, {plan_id}: {text}\n"
        
        if len(context) > max_length:
            break

    return context
