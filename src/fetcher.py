
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import List
from config.config import API_URL_TEMPLATE
from src.logger import get_logger

logger = get_logger(__name__)

# --- Setup session with retry ---
def get_retry_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=3,                # total retry attempts
        backoff_factor=2,       # wait 2s, then 4s, then 8s
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def fetch_data_for_month(force_id: str, year: int, month: int) -> List[dict]:
    session = get_retry_session()
    date_str = f"{year}-{month:02d}"
    url = API_URL_TEMPLATE.format(force=force_id, date=date_str)
    logger.info(f"Fetching data for {date_str}...")

    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data for {date_str}: {e}")
        return []