from abc import ABC, abstractmethod
from typing import List, Dict

class FeedbackRepository(ABC):
    @abstractmethod
    def setup_database(self):
        """Initialize the database and create tables if necessary."""
        pass

    @abstractmethod
    def store_feedback(self, model: str, user_input: str, output: str) -> bool:
        """Store feedback data."""
        pass

    @abstractmethod
    def retrieve_feedback(self) ->  List[Dict]:
        """Retrieve all feedback data."""
        pass

    @abstractmethod
    def delete_all(self):
        """Delete all feedback data."""
        pass
