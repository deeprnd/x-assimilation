import json
import os

from services.data.base_storage import BaseStorage


class JSONStorage (BaseStorage):
    """Manages JSON storage for processed tweets."""
    def __init__(self, filename):
        self.filename = filename
        if os.path.exists(self.filename):
            self.data = self._load_data()
        else:
            self.data = []
            self._save_data()

    def _load_data(self):
        """Load tweet history from file."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                return json.load(file)
        return []

    def _save_data(self):
        """Save tweet history to file."""
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=2)

    def add_processed_tweet(self, tweet_id, tweet_datetime, tweet_text, response_text):
        """Store a processed tweet."""
        self.data.append({
            "id": tweet_id,
            "time": tweet_datetime,
            "tweet": tweet_text,
            "response": response_text
        })
        self._save_data()

    def is_tweet_processed(self, tweet_id):
        """Check if tweet was already processed."""
        return any(t["id"] == tweet_id for t in self.data)