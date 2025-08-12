import os
import logging
from config.config import LOG_PATH

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger that logs to both console and a file.

    Ensures:
    - Log directory exists
    - Handlers are explicitly added so it works even if logging was already configured
    """
    # Ensure log directory exists
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Remove any existing handlers to prevent duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    # Formatter for logs
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # File handler
    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger