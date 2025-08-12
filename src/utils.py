from datetime import datetime, timedelta
from typing import List, Tuple
import pandas as pd
from src.logger import get_logger

logger = get_logger(__name__)

def get_months_to_fetch(last_update_date: datetime, current_date: datetime) -> List[Tuple[int, int]]:
    """
    Determines the list of year-month pairs that need to be fetched from the API.

    Args:
        last_update_date (datetime): The most recent date for which data is already stored.
        current_date (datetime): The current date (used to determine the upper limit).

    Returns:
        List[Tuple[int, int]]: A list of (year, month) tuples representing missing months.
    """
    months = []

    # Move to the first day of the month after the last update
    start_date = (last_update_date + timedelta(days=32)).replace(day=1)

    # Loop until reaching the current month
    while start_date <= current_date.replace(day=1):
        # Append year-month tuple for the current start_date
        months.append((start_date.year, start_date.month))
        
        # Move to the first day of the next month
        start_date = (start_date + timedelta(days=32)).replace(day=1)

    return months


def clean_and_format_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and standardizes a DataFrame for consistent processing.

    Args:
        df (pd.DataFrame): The DataFrame containing stop-and-search data.

    Returns:
        pd.DataFrame: The cleaned and formatted DataFrame.
    """
    # If DataFrame is empty, log a warning and return as-is
    if df.empty:
        logger.warning("Received empty DataFrame to clean.")
        return df

    # Remove rows where all columns are NaN
    df.dropna(how='all', inplace=True)

    # Standardize column names: lowercase and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    # Convert 'datetime' column to datetime objects if present
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

    logger.info("Data cleaned and formatted.")
    return df