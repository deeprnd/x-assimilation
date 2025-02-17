from logging import Logger
import random
import time
from services.llm.llm_invoker import LLMInvoker
from services.social.social_manager import SocialManager

class AssimilationManager(Logger):
    """Class to social network assimilation."""

    def __init__(self, 
                 social_manager: SocialManager,
                 llm_invoker: LLMInvoker):
        self.social_manager = social_manager
        self.llm_invoker = llm_invoker

    async def assimilate(self):
        """Assimilate the social network."""
        try:
            posts = self.social_manager.fetch_recent_posts()
            most_liked, most_retweeted = self.social_manager.get_most_liked_and_commented(posts)
        except Exception as e:
            await self.social_manager.sleep()
            self.logger.error(f"Error fetching recent posts: {e}")

        if not most_liked and not most_retweeted:
            self.logger.warning("No new tweets to process. Sleeping...")
            await self.social_manager.sleep()
            return
