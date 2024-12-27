from typing import List

def format_context(search_results: List[dict], max_length: int = 10000) -> str:
    """Format Qdrant search results for context."""
    context = ""
    try:
        for result in search_results:
            payload = result.payload
            field = payload.get("Field", "Unknown Field")
            plan_name = payload.get("Plan_Name", "Unknown Plan ID")
            text = payload.get("Full Text", "No text available")
            context += f"- {field}, {plan_name}: {text}\n"
            
            if len(context) > max_length:
                break
    except Exception as e:
        print(f"Error formatting context: {e}")
    return context
