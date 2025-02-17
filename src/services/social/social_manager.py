from abc import ABC, abstractmethod
from logging import Logger
from typing import Optional

class SocialManager(ABC, Logger):
    """Abstract base class for social network managers."""
    
    @abstractmethod
    def fetch_recent_posts(self):
        """Fetch recent tweets based on search criteria."""
        pass 

    @abstractmethod
    def get_most_liked_and_commented(self, posts):
        """Fetch two posts, to the most liked, and the most commented."""
        pass

    @abstractmethod
    async def sleep(self):
        """Sleep for a random amount of time."""
        pass