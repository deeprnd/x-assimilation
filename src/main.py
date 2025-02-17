import asyncio
import os
from dotenv import load_dotenv
from services.assimilation.assimilation_manager import AssimilationManager
from services.llm.ollama_invoker import OllamaInvoker
from services.social.x_manager import TwitterCredentials, XManager
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger()

async def assimilate_x():
    try:
        x_manager = XManager(
            credentials=TwitterCredentials(
                bearer_token=os.getenv("TWITTER_BEARER_TOKEN")
            ),
            me=os.getenv("TWITTER_USERNAME"),
            hashtags=os.getenv("TWITTER_HASHTAGS", "").split(","),
            accounts=os.getenv("TWITTER_ACCOUNTS", "").split(","),
            hours_back=int(os.getenv("TWITTER_HOURS_BACK", "24")),
            top_tweets=int(os.getenv("TWITTER_TOP_TWEETS", "100")),
            max_sleep_minutes=int(os.getenv("TWITTER_MAX_SLEEP_MINUTES", "60"))
        )
        ollama_invoker = OllamaInvoker(
            api_url=os.getenv("LLM_API_URL"),
            model=os.getenv("LLM_MODEL")
        )
        assimilation_manager = AssimilationManager(x_manager, ollama_invoker)
        await assimilation_manager.assimilate()
    except Exception as e:
        logger.error(f"Error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(assimilate_x()) 