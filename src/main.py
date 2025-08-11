from src.updater import update_data
from src.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    try:
        update_data()
    except Exception as e:
        logger.exception("Unhandled exception during data update.")