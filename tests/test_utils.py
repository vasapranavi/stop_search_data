import pandas as pd
import pytest
from datetime import datetime
# from police_data_updater.utils import get_months_to_fetch, clean_and_format_dataframe
from src.utils import get_months_to_fetch, clean_and_format_dataframe

def test_get_months_to_fetch():
    start = datetime(2023, 1, 1)
    end = datetime(2023, 3, 1)
    result = get_months_to_fetch(start, end)
    assert result == [(2023, 2), (2023, 3)]

def test_clean_and_format_dataframe():
    raw_data = {
        "Datetime": ["2023-01-01T00:00:00Z"],
        "Outcome": ["No further action"],
        "Extra": [{"nested": "value"}]
    }
    df = pd.DataFrame(raw_data)
    cleaned = clean_and_format_dataframe(df)
    assert "datetime" in cleaned.columns
    assert "Extra" not in cleaned.columns or "extra" not in cleaned.columns
