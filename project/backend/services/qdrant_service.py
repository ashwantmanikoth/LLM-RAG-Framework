# my_app/qdrant_service.py
from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from utils.config import Config

qdrant_client = QdrantClient(url=Config.QDRANT_URL)

def search_qdrant(
    query_embedding: List[float],
    zip_code: str,
    top_k: int = 20,
    score_threshold: float = 0.7
) -> List[Dict]:
    """
    Search Qdrant for relevant results.
    """
    try:
        results = qdrant_client.search(
        collection_name=Config.COLLECTION_NAME,
        query_vector=query_embedding,
        query_filter=Filter(
            must=[
                FieldCondition(key="Zip_code", match=MatchValue(value=zip_code))
            ]
        ),
        score_threshold=score_threshold,
        limit=top_k,
        with_payload=True,
    )
        filtered_results = [
            result for result in results
            if result.payload.get("Field") in ["Benefits", "Extra Details"]
        ]
        if not filtered_results:
            return results
        
        print(f"Qdrant search results: {results}")    
        return filtered_results

    except Exception as e:
        print(f"Error during Qdrant search: {e}")
        return []
