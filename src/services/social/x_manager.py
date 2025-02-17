import asyncio
import random
from services.social.social_manager import SocialManager
import tweepy
from datetime import datetime, timedelta, timezone


class TwitterCredentials:
    """Class to store Twitter API credentials."""
    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token

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
        # Authenticate with Twitter using v2 API
        self.client = tweepy.Client(
            bearer_token=credentials.bearer_token,
            wait_on_rate_limit=True
        )
        
        # Initialize parameters
        self.hashtags = hashtags
        self.accounts = accounts
        self.hours_back = hours_back
        self.top_tweets = top_tweets
        self.max_sleep_minutes = max_sleep_minutes
        self.me = me

    def _build_search_query(self):
        """Dynamically generate search query from hashtags and accounts."""
        hashtag_query = " OR ".join([tag.strip() for tag in self.hashtags])
        account_query = " OR ".join([f"from:{acc.strip()}" for acc in self.accounts])
        
        # Note: Twitter API v2 uses different time format
        since_time = (datetime.now(timezone.utc) - timedelta(hours=self.hours_back)).strftime("%Y-%m-%dT%H:%M:%SZ")
        query = f"({hashtag_query}) OR ({account_query})"
        
        return query, since_time

    def fetch_recent_posts(self):
        """Fetch recent tweets based on search criteria."""
        query, start_time = self._build_search_query()
        
        # Using v2 API with tweet metrics
        response = self.client.search_recent_tweets(
            query=query,
            max_results=self.top_tweets,
            start_time=start_time,
            tweet_fields=['public_metrics', 'author_id'],
            user_fields=['username']
        )
        
        if not response.data:
            return []
        
        resp = []
        for tweet in response.data:
            if not self.storage.is_processed(tweet.id) and tweet.author_id != self.me:
                resp.append(tweet)
        
        return resp
    
    def get_most_liked_and_commented(self, posts):
        """Fetch two posts: the most liked and the most retweeted."""
        if not posts:
            return None, None

        # In v2 API, metrics are in public_metrics dictionary
        tweets_by_likes = sorted(posts, key=lambda t: t.public_metrics['like_count'], reverse=True)
        most_liked = tweets_by_likes[0] if tweets_by_likes else None

        tweets_by_retweets = sorted(posts, key=lambda t: t.public_metrics['retweet_count'], reverse=True)
        most_retweeted = tweets_by_retweets[0] if tweets_by_retweets else None

        return most_liked, most_retweeted
    
    async def sleep(self):
        """Sleep for a random amount of time."""
        await asyncio.sleep(random.randint(1, self.max_sleep_minutes) * 60)