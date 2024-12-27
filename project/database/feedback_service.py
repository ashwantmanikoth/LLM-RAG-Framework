from typing import List, Dict, Any
from database.feedback_repository import FeedbackRepository


class FeedbackService:
    def __init__(self, repository: FeedbackRepository):
        self.repository = repository

    def add_feedback(self, model: str, user_input: str, output: str) -> bool:
        """Add feedback data."""
        return self.repository.store_feedback(model, user_input, output)

    def get_feedback(self) -> List[Dict]:
        """Retrieve feedback data."""
        return self.repository.retrieve_feedback()

    def delete_feedback(self):
        """Delete all feedback data."""
        self.repository.delete_all()
