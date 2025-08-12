import os
import time
from datetime import datetime
import pandas as pd
from typing import Tuple

from config.config import CSV_FILE, EARLIEST_DATA_DATE, FORCE_ID
from src.logger import get_logger
from src.utils import get_months_to_fetch, clean_and_format_dataframe
from src.fetcher import fetch_data_for_month

logger = get_logger(__name__)

def read_existing_data(file_path: str) -> Tuple[pd.DataFrame, datetime]:
    """
    Reads existing stop-and-search data from a CSV file if it exists.

    Args:
        file_path (str): Path to the CSV file containing historical data.

    Returns:
        Tuple[pd.DataFrame, datetime]:
            - DataFrame with the loaded data (empty if file missing or unreadable).
            - Datetime of the most recent record (defaults to EARLIEST_DATA_DATE if missing).

    Notes:
        - If the CSV file is missing or cannot be read, an empty DataFrame and
          the earliest date constant are returned to start fresh.
        - The 'datetime' column is parsed into timezone-naive datetime objects.
    """
    # If CSV file doesn't exist, start with empty DataFrame and earliest date
    if not os.path.exists(file_path):
        logger.info(f"No existing data found at '{file_path}'. Starting fresh.")
        return pd.DataFrame(), EARLIEST_DATA_DATE

    try:
        # Load CSV into DataFrame
        df = pd.read_csv(file_path)

        # Parse 'datetime' column into proper datetime objects (remove timezone)
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce').dt.tz_localize(None)

        # Get the latest date in the dataset
        last_update = df['datetime'].max()

        logger.info(f"Existing data loaded. Last update: {last_update.date()}")
        return df, last_update

    except Exception as e:
        # If reading/parsing fails, log a warning and start fresh
        logger.warning(f"Failed to read existing CSV: {e}. Starting fresh.")
        return pd.DataFrame(), EARLIEST_DATA_DATE


def update_data() -> None:
    """
    Updates the local stop-and-search dataset with the latest data from the API.

    Process:
        1. Reads existing CSV data (or starts fresh if none found).
        2. Determines which months' data are missing.
        3. Fetches new monthly data from the API.
        4. Cleans, formats, and appends new data to the existing dataset.
        5. Saves the updated dataset back to CSV.

    Returns:
        None
    """
    logger.info("Starting update process...")

    # Load existing dataset and determine last update date
    existing_df, last_update_date = read_existing_data(CSV_FILE)

    # Determine current date and calculate missing months
    current_date = datetime.now()
    months_to_fetch = get_months_to_fetch(last_update_date, current_date)

    # Exit early if there is no new data to fetch
    if not months_to_fetch:
        logger.info("No new months to fetch. Data is up to date.")
        return

    new_records = []

    # Fetch new data month-by-month
    for year, month in months_to_fetch:
        month_data = fetch_data_for_month(FORCE_ID, year, month)
        if month_data:
            new_records.extend(month_data)
        time.sleep(1)  # Avoid overwhelming the API

    # Exit if no new data was retrieved
    if not new_records:
        logger.warning("No new data retrieved from the API.")
        return

    # Create DataFrame for new data
    new_df = pd.DataFrame(new_records)

    # Combine with existing data
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)

    # Clean and format the combined dataset
    cleaned_df = clean_and_format_dataframe(combined_df)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

    # Save the updated dataset to CSV
    cleaned_df.to_csv(CSV_FILE, index=False)
    logger.info(f"Data successfully updated and saved to '{CSV_FILE}'.")