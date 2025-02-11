import pytest
from unittest.mock import Mock, patch
import requests
from services.llm.ollama_invoker import OllamaInvoker

API_URL = "http://localhost:11434/api/generate"
MODEL = "llama2"

@pytest.fixture
def ollama_invoker():
    """Create an OllamaInvoker instance."""
    invoker = OllamaInvoker(API_URL, MODEL)
    # Initialize logger mock
    invoker.logger = Mock()
    invoker.level = Mock()
    invoker.name = Mock()
    return invoker

def test_init():
    """Test OllamaInvoker initialization."""
    invoker = OllamaInvoker(API_URL, MODEL)
    assert invoker.api_url == API_URL
    assert invoker.model == MODEL

def test_invoke_successful(ollama_invoker):
    """Test successful API call."""
    expected_response = "This is a test response"
    mock_response = Mock()
    mock_response.json.return_value = {"response": expected_response}
    
    with patch('requests.post') as mock_post:
        mock_post.return_value = mock_response
        
        result = ollama_invoker.invoke("Test prompt")
        
        # Verify the result
        assert result == expected_response
        
        # Verify the API was called correctly
        mock_post.assert_called_once_with(
            API_URL,
            json={
                "model": MODEL,
                "prompt": "Test prompt",
                "stream": False
            }
        )

def test_invoke_api_error(ollama_invoker):
    """Test API call with error."""
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.exceptions.HTTPError("API Error")
        
        result = ollama_invoker.invoke("Test prompt")
        
        # Verify error handling
        assert result is None
        ollama_invoker.logger.error.assert_called_once()
        assert "API Error" in ollama_invoker.logger.error.call_args[0][0]

def test_invoke_empty_response(ollama_invoker):
    """Test API call with empty response."""
    mock_response = Mock()
    mock_response.json.return_value = {}
    
    with patch('requests.post') as mock_post:
        mock_post.return_value = mock_response
        
        result = ollama_invoker.invoke("Test prompt")
        
        # Verify handling of empty response
        assert result is None

def test_invoke_http_error(ollama_invoker):
    """Test API call with HTTP error."""
    with patch('requests.post') as mock_post:
        mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("HTTP Error")
        
        result = ollama_invoker.invoke("Test prompt")
        
        # Verify error handling
        assert result is None
        ollama_invoker.logger.error.assert_called_once()
        assert "HTTP Error" in ollama_invoker.logger.error.call_args[0][0] 