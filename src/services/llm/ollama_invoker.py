from typing import Optional
import requests
from .llm_invoker import LLMInvoker

class OllamaInvoker(LLMInvoker):
    """Invoker for Ollama API responses."""
    
    def __init__(self, api_url: str, model: str):
        """
        Initialize OllamaInvoker with API URL and model type.
        :param api_url: The Ollama API endpoint (e.g., http://localhost:11434/api/generate)
        :param model: The LLM model to use (e.g., deepseek-r1:1.5b)
        """
        self.api_url = api_url
        self.model = model

    def invoke(self, prompt: str) -> Optional[str]:
        """
        Calls the Ollama API and extracts the response.
        :param prompt: The input prompt for the LLM.
        :return: The generated response as a string, or None if an error occurs.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()  # Raise error for HTTP issues
            data = response.json()
            return data.get("response")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error calling Ollama API: {e}")
            return None 