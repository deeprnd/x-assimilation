import logging
import os

class Logger:
    def __init__(self):
        log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # Create logger
        self.logger = logging.getLogger("llm_project")
        self.logger.setLevel(log_level)
        
        # Create console handler and set level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Add formatter to console handler
        console_handler.setFormatter(formatter)
        
        # Add console handler to logger
        self.logger.addHandler(console_handler)