
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import List
from config.config import API_URL_TEMPLATE
from src.logger import get_logger

logger = get_logger(__name__)

# --- Setup session with retry ---
def get_retry_session() -> requests.Session:
    """
    Creates and configures a `requests.Session` with retry logic for resilient HTTP requests.

    This session will automatically retry failed GET requests up to 3 times, using
    exponential backoff (2 seconds, 4 seconds, 8 seconds) for certain HTTP status codes
    that are considered transient errors.

    Returns:
        requests.Session: A configured session object that can be used for making
        HTTP GET requests with built-in retry handling.

    Retry Configuration:
        - total=3: Retry a maximum of 3 times before giving up.
        - backoff_factor=2: The delay between retries increases exponentially (2s → 4s → 8s).
        - status_forcelist: Retries are triggered for HTTP status codes:
            429 (Too Many Requests)
            500 (Internal Server Error)
            502 (Bad Gateway)
            503 (Service Unavailable)
            504 (Gateway Timeout)
        - allowed_methods=["GET"]: Retries are applied only to GET requests.
    """
    session = requests.Session()

    # Configure retry strategy:
    retry = Retry(
        total=3,                # Max number of retry attempts
        backoff_factor=2,       # Delay grows exponentially: 2s, 4s, 8s
        status_forcelist=[429, 500, 502, 503, 504],  # Retry only for these status codes
        allowed_methods=["GET"] # Apply retries only to GET requests
    )

    # Create HTTP adapter with the retry policy
    adapter = HTTPAdapter(max_retries=retry)

    # Mount the adapter to handle both HTTP and HTTPS requests
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def fetch_data_for_month(force_id: str, year: int, month: int) -> List[dict]:
    """
    About:
        Retrieves stop-and-search data for a given police force and month 
        from the UK Police API using a retry-enabled session.

    Inputs:
        force_id (str)  - Unique ID of the police force.
        year (int)      - Year of the data to fetch (YYYY format).
        month (int)     - Month of the data to fetch (1–12).

    Outputs:
        List[dict] - Parsed JSON data from the API, or an empty list on failure.
    """
    # Create an HTTP session with retry/backoff policy
    session = get_retry_session()

    # Format date into YYYY-MM for the API request
    date_str = f"{year}-{month:02d}"

    # Build API URL for the given force and date
    url = API_URL_TEMPLATE.format(force=force_id, date=date_str)
    logger.info(f"Fetching data for {date_str}...")

    try:
        # Make GET request to the API
        response = session.get(url, timeout=15)
        response.raise_for_status()  # Raise an error for HTTP 4xx/5xx
        return response.json()       # Return JSON data as a Python object
    except requests.RequestException as e:
        # Log the error and return an empty list on failure
        logger.error(f"Error fetching data for {date_str}: {e}")
        return []