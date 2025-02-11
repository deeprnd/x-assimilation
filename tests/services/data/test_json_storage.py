import pytest
import os
import json
from services.data.json_storage import JSONStorage

@pytest.fixture
def temp_json_file(tmp_path):
    """Create a temporary JSON file for testing."""
    file_path = tmp_path / "test_tweets.json"
    return str(file_path)

@pytest.fixture
def storage(temp_json_file):
    """Create a JSONStorage instance with a temporary file."""
    return JSONStorage(temp_json_file)

def test_init_new_file(temp_json_file):
    """Test initialization with a new file."""
    storage = JSONStorage(temp_json_file)
    assert storage.data == []
    assert os.path.exists(temp_json_file)

def test_init_existing_file(temp_json_file):
    """Test initialization with existing data."""
    initial_data = [{"id": "123", "time": "2024-01-01", "tweet": "test", "response": "reply"}]
    with open(temp_json_file, "w") as f:
        json.dump(initial_data, f)
    
    storage = JSONStorage(temp_json_file)
    assert storage.data == initial_data

def test_add_processed_tweet(storage):
    """Test adding a new processed tweet."""
    storage.add_processed_tweet("123", "2024-01-01", "test tweet", "test response")
    
    assert len(storage.data) == 1
    assert storage.data[0]["id"] == "123"
    assert storage.data[0]["tweet"] == "test tweet"
    
    # Verify data was saved to file
    with open(storage.filename, "r") as f:
        saved_data = json.load(f)
    assert saved_data == storage.data

def test_is_tweet_processed(storage):
    """Test checking if a tweet was processed."""
    storage.add_processed_tweet("123", "2024-01-01", "test tweet", "test response")
    
    assert storage.is_tweet_processed("123") is True
    assert storage.is_tweet_processed("456") is False 