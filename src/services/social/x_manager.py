from services.social.social_manager import SocialManager
import tweepy
from datetime import datetime, timedelta, timezone


class TwitterCredentials:
    """Class to store Twitter API credentials."""
    def __init__(self, api_key: str, api_secret: str, access_token: str, access_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_secret = access_secret

class XManager(SocialManager):
    """Class to manage X social network."""

    def __init__(self, 
                 credentials: TwitterCredentials,
                 me: str,
                 hashtags: list[str],
                 accounts: list[str],
                 hours_back: int,
                 top_tweets: int,
                 max_sleep_minutes: int):
        # Authenticate with Twitter
        auth = tweepy.OAuth1UserHandler(
            credentials.api_key,
            credentials.api_secret,
            credentials.access_token,
            credentials.access_secret
        )
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        
        # Initialize parameters with defaults if not provided
        self.hashtags = hashtags
        self.accounts = accounts
        self.hours_back = hours_back
        self.top_tweets = top_tweets
        self.max_sleep_minutes = max_sleep_minutes
        self.me = me

    def _build_search_query(self):
        """Dynamically generate search query from hashtags and accounts."""
        hashtag_query = " OR ".join(self.hashtags)
        account_query = " OR ".join([f"from:{acc}" for acc in self.accounts])
        
        since_time = (datetime.now(timezone.utc) - timedelta(hours=self.hours_back)).strftime("%Y-%m-%d_%H:%M:%S_UTC")
        query = f"({hashtag_query}) OR ({account_query}) since:{since_time}"
        
        return query

    def fetch_recent_posts(self):
        """Fetch recent tweets based on search criteria."""
        query = self._build_search_query()
        tweets = self.api.search_tweets(q=query, count=self.top_tweets, result_type="recent", tweet_mode="extended")
        
        for tweet in tweets:
            if not self.storage.is_processed(tweet.id) and tweet.user.screen_name != self.me:
                return tweet  # Return only the first unprocessed tweet
        return None