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
    if not os.path.exists(file_path):
        logger.info(f"No existing data found at '{file_path}'. Starting fresh.")
        return pd.DataFrame(), EARLIEST_DATA_DATE

    try:
        df = pd.read_csv(file_path)
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce').dt.tz_localize(None)
        last_update = df['datetime'].max()
        logger.info(f"Existing data loaded. Last update: {last_update.date()}")
        return df, last_update
    except Exception as e:
        logger.warning(f"Failed to read existing CSV: {e}. Starting fresh.")
        return pd.DataFrame(), EARLIEST_DATA_DATE


def update_data() -> None:
    logger.info("Starting update process...")

    existing_df, last_update_date = read_existing_data(CSV_FILE)
    current_date = datetime.now()
    months_to_fetch = get_months_to_fetch(last_update_date, current_date)

    if not months_to_fetch:
        logger.info("No new months to fetch. Data is up to date.")
        return

    new_records = []
    for year, month in months_to_fetch:
        month_data = fetch_data_for_month(FORCE_ID, year, month)
        if month_data:
            new_records.extend(month_data)
        time.sleep(1)

    if not new_records:
        logger.warning("No new data retrieved from the API.")
        return

    new_df = pd.DataFrame(new_records)
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    cleaned_df = clean_and_format_dataframe(combined_df)
    # Ensure output directory exists
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

    # Write to CSV
    cleaned_df.to_csv(CSV_FILE, index=False)
    logger.info(f"Data successfully updated and saved to '{CSV_FILE}'.")