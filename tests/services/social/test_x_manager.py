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
    return TwitterCredentials(bearer_token="test_bearer_token")

@pytest.fixture
def mock_storage():
    """Create a mock storage instance."""
    storage = Mock()
    storage.is_processed.return_value = False
    return storage

@pytest.fixture
def mock_tweepy_client():
    """Create a mock Tweepy Client."""
    with patch('tweepy.Client') as mock_client:
        yield mock_client.return_value

@pytest.fixture
def x_manager(credentials, mock_tweepy_client, mock_storage):
    """Create an XManager instance with mocked dependencies."""
    manager = XManager(
        credentials=credentials,
        hashtags=HASHTAGS,
        accounts=ACCOUNTS,
        hours_back=HOURS_BACK,
        top_tweets=TOP_TWEETS,
        max_sleep_minutes=MAX_SLEEP_MINUTES,
        me=ME
    )
    manager.client = mock_tweepy_client
    manager.storage = mock_storage
    return manager

def test_init(credentials):
    """Test XManager initialization."""
    with patch('tweepy.Client'):
        manager = XManager(credentials, me=ME, hashtags=HASHTAGS, accounts=ACCOUNTS, 
                         hours_back=HOURS_BACK, top_tweets=TOP_TWEETS, max_sleep_minutes=MAX_SLEEP_MINUTES)
        
        assert manager.hashtags == HASHTAGS
        assert manager.accounts == ACCOUNTS
        assert manager.hours_back == HOURS_BACK
        assert manager.top_tweets == TOP_TWEETS
        assert manager.max_sleep_minutes == MAX_SLEEP_MINUTES
        assert manager.me == ME

def test_build_search_query(x_manager):
    """Test search query building."""
    with patch('datetime.datetime') as mock_datetime:
        mock_now = datetime.now(timezone.utc)
        mock_datetime.now.return_value = mock_now
        
        query, start_time = x_manager._build_search_query()
        expected_time = (mock_now - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
        expected_query = "(#Test) OR (from:testuser)"
        
        assert query == expected_query
        assert start_time == expected_time

def test_fetch_recent_posts_no_tweets(x_manager):
    """Test fetching posts when no tweets are found."""
    mock_response = Mock()
    mock_response.data = None
    x_manager.client.search_recent_tweets.return_value = mock_response
    
    result = x_manager.fetch_recent_posts()
    assert result == []
    assert x_manager.client.search_recent_tweets.called

def test_fetch_recent_posts_with_tweets(x_manager):
    """Test fetching posts with available tweets."""
    mock_tweet = Mock()
    mock_tweet.id = "123"
    mock_tweet.author_id = "testuser1"
    
    mock_response = Mock()
    mock_response.data = [mock_tweet]
    x_manager.client.search_recent_tweets.return_value = mock_response
    
    result = x_manager.fetch_recent_posts()
    assert result == [mock_tweet]
    x_manager.storage.is_processed.assert_called_with("123")

def test_fetch_recent_posts_with_my_tweets(x_manager):
    """Test fetching posts excluding own tweets."""
    mock_tweet = Mock()
    mock_tweet.id = "123"
    mock_tweet.author_id = ME
    
    mock_response = Mock()
    mock_response.data = [mock_tweet]
    x_manager.client.search_recent_tweets.return_value = mock_response
    
    result = x_manager.fetch_recent_posts()
    assert result == []

def test_get_most_liked_and_commented_no_tweets(x_manager):
    """Test getting most liked and retweeted posts when no tweets are available."""
    posts = []
    most_liked, most_retweeted = x_manager.get_most_liked_and_commented(posts)
    assert most_liked is None
    assert most_retweeted is None

def test_get_most_liked_and_commented_with_tweets(x_manager):
    """Test getting most liked and retweeted posts with available tweets."""
    tweet1 = Mock()
    tweet1.public_metrics = {'like_count': 10, 'retweet_count': 5}

    tweet2 = Mock()
    tweet2.public_metrics = {'like_count': 5, 'retweet_count': 15}

    tweet3 = Mock()
    tweet3.public_metrics = {'like_count': 3, 'retweet_count': 2}

    posts = [tweet1, tweet2, tweet3]
    
    most_liked, most_retweeted = x_manager.get_most_liked_and_commented(posts)
    
    assert most_liked == tweet1  # most likes (10)
    assert most_retweeted == tweet2  # most retweets (15)