from datetime import datetime, timedelta
from typing import List, Tuple
import pandas as pd
from src.logger import get_logger

logger = get_logger(__name__)

def get_months_to_fetch(last_update_date: datetime, current_date: datetime) -> List[Tuple[int, int]]:
    months = []
    start_date = (last_update_date + timedelta(days=32)).replace(day=1)

    while start_date <= current_date.replace(day=1):
        months.append((start_date.year, start_date.month))
        start_date = (start_date + timedelta(days=32)).replace(day=1)

    return months


def clean_and_format_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        logger.warning("Received empty DataFrame to clean.")
        return df

    df.dropna(how='all', inplace=True)
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

    logger.info("Data cleaned and formatted.")
    return df