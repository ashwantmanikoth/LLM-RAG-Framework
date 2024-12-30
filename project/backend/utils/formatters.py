from typing import List

def format_context(search_results: List[dict], max_length: int = 10000) -> str:
    """Format Qdrant search results for context."""
    context = []
    context.append("```CONTEXT_START```")
    try:
        for result in search_results:
            payload = result.payload
            field = payload.get("Field", "")
            plan_name = payload.get("Plan_Name", "")
            text = payload.get("Full Text", "")
            context.append(f"{plan_name} - {text}\n")
            if sum(len(s) for s in context) > max_length:
                break
    except Exception as e:
        print(f"Error formatting context: {e}")

    context.append("```CONTEXT_END```")
    return ''.join(context)
