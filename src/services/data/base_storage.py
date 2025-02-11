from abc import ABC, abstractmethod
from logging import Logger

class BaseStorage(ABC, Logger):
    """Abstract base class for storage implementations."""
    
    @abstractmethod
    def add_processed_tweet(self, tweet_id, tweet_datetime, tweet_text, response_text):
        """Store a processed tweet."""
        pass

    @abstractmethod
    def is_tweet_processed(self, tweet_id):
        """Check if tweet was already processed."""
        pass