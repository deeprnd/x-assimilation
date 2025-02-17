import logging
import os

class Logger:
    def __init__(self):
        self.logger = setup_logger()

def setup_logger():
    log_level = os.getenv("LOG_LEVEL", "INFO")
    
    # Create logger
    logger = logging.getLogger("llm_project")
    logger.setLevel(log_level)
    
    # Create console handler and set level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Add formatter to console handler
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger