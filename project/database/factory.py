import os
from database.sqlite_feedback_repository import SQLiteFeedbackRepository

def load_properties(file_path: str) -> dict:
    """Load properties from a configuration file."""
    properties = {}
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            for line in f:
                # Ignore comments and blank lines
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    properties[key.strip()] = value.strip()
    return properties


def get_repository() -> object:
    """Factory method to return the appropriate repository instance."""
    # Load the properties
    properties = load_properties("config.properties")
    db_type = properties.get("db_type", "sqlite").lower()

    if db_type == "sqlite":
        db_file = properties.get("db_file", "default.db")
        return SQLiteFeedbackRepository(db_file)

    else:
        raise ValueError(f"Unsupported database type: {db_type}")
