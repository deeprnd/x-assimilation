import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta, timezone
from services.social.x_manager import XManager, TwitterCredentials

ME="testuser"
HASHTAGS=["#Test"]
ACCOUNTS=["testuser"]
HOURS_BACK=24
TOP_TWEETS=10
MAX_SLEEP_MINUTES=30

@pytest.fixture
def credentials():
    """Create test Twitter credentials."""
    return TwitterCredentials(
        api_key="test_key",
        api_secret="test_secret",
        access_token="test_token",
        access_secret="test_secret"
    )

@pytest.fixture
def mock_storage():
    """Create a mock storage instance."""
    storage = Mock()
    storage.is_processed.return_value = False
    return storage

@pytest.fixture
def mock_tweepy_api():
    """Create a mock Tweepy API."""
    with patch('tweepy.API') as mock_api:
        yield mock_api.return_value

@pytest.fixture
def x_manager(credentials, mock_tweepy_api, mock_storage):
    """Create an XManager instance with mocked dependencies."""
    with patch('tweepy.OAuth1UserHandler'):
        manager = XManager(
            credentials=credentials,
            hashtags=HASHTAGS,
            accounts=ACCOUNTS,
            hours_back=HOURS_BACK,
            top_tweets=TOP_TWEETS,
            max_sleep_minutes=MAX_SLEEP_MINUTES,
            me=ME
        )
        manager.api = mock_tweepy_api
        manager.storage = mock_storage
        return manager

def test_init(credentials):
    """Test XManager initialization."""
    with patch('tweepy.OAuth1UserHandler'), patch('tweepy.API'):
        me = "testuser"
        manager = XManager(credentials, me=me, hashtags=HASHTAGS, accounts=ACCOUNTS, hours_back=HOURS_BACK, top_tweets=TOP_TWEETS, max_sleep_minutes=MAX_SLEEP_MINUTES)
        
        assert manager.hashtags == HASHTAGS
        assert manager.accounts == ACCOUNTS
        assert manager.hours_back == HOURS_BACK
        assert manager.top_tweets == TOP_TWEETS
        assert manager.max_sleep_minutes == MAX_SLEEP_MINUTES
        assert manager.me == me

def test_build_search_query(x_manager):
    """Test search query building."""
    with patch('datetime.datetime') as mock_datetime:
        mock_now = datetime.now(timezone.utc)
        mock_datetime.now.return_value = mock_now
        
        query = x_manager._build_search_query()
        expected_time = (mock_now - timedelta(hours=24)).strftime("%Y-%m-%d_%H:%M:%S_UTC")
        expected_query = f"(#Test) OR (from:testuser) since:{expected_time}"
        
        assert query == expected_query

def test_fetch_recent_posts_no_tweets(x_manager):
    """Test fetching posts when no tweets are found."""
    x_manager.api.search_tweets.return_value = []
    
    result = x_manager.fetch_recent_posts()
    assert result is None
    assert x_manager.api.search_tweets.called

def test_fetch_recent_posts_with_tweets(x_manager):
    """Test fetching posts with available tweets."""
    mock_tweet = Mock()
    mock_tweet.id = "123"
    mock_tweet.user.screen_name = "testuser1"
    x_manager.api.search_tweets.return_value = [mock_tweet]
    
    result = x_manager.fetch_recent_posts()
    assert result == mock_tweet
    x_manager.storage.is_processed.assert_called_with("123")

def test_fetch_recent_posts_with_my_tweets(x_manager):
    """Test fetching posts with available tweets."""
    mock_tweet = Mock()
    mock_tweet.id = "123"
    mock_tweet.user.screen_name = ME
    x_manager.api.search_tweets.return_value = [mock_tweet]
    
    result = x_manager.fetch_recent_posts()
    assert result == None