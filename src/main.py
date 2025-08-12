from src.updater import update_data
from src.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    """
    About:
        Entry point for running the script directly.
        Attempts to update police stop-and-search data.

    Behavior:
        Calls update_data() and logs any unhandled exceptions
        with a full traceback for debugging.
    """
    try:
        update_data()
    except Exception as e:
        logger.exception("Unhandled exception during data update.")