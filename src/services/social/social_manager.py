from abc import ABC, abstractmethod
from logging import Logger
from typing import Optional

class SocialManager(ABC, Logger):
    """Abstract base class for social network managers."""
    
    @abstractmethod
    def fetch_recent_posts(self):
        """Fetch recent tweets based on search criteria."""
        pass 