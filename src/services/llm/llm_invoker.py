from abc import ABC, abstractmethod
from logging import Logger
from typing import Optional

class LLMInvoker(ABC, Logger):
    """Abstract base class for LLM invokers."""
    
    @abstractmethod
    def invoke(self, prompt: str) -> Optional[str]:
        """Call LLM API and return response."""
        pass 