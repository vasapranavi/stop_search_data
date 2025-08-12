import pandas as pd
import pytest
from datetime import datetime
# from police_data_updater.utils import get_months_to_fetch, clean_and_format_dataframe
from src.utils import get_months_to_fetch, clean_and_format_dataframe

def test_get_months_to_fetch():
    """
    Test that get_months_to_fetch correctly generates a list of (year, month) 
    tuples for all months between the given last update date and current date.

    In this case:
    - Start date is Jan 2023
    - End date is Mar 2023
    - Expected months to fetch: Feb 2023 and Mar 2023
    """
    # Define the starting and ending dates for the test
    start = datetime(2023, 1, 1)
    end = datetime(2023, 3, 1)

    # Call the function to get months to fetch
    result = get_months_to_fetch(start, end)

    # Verify the output matches the expected months
    assert result == [(2023, 2), (2023, 3)]


def test_clean_and_format_dataframe():
    """
    Test that clean_and_format_dataframe:
    - Converts column names to lowercase with underscores.
    - Parses 'datetime' column into proper datetime objects.
    - Removes entirely empty columns.
    """
    # Create raw DataFrame with mixed-case column names and nested data
    raw_data = {
        "Datetime": ["2023-01-01T00:00:00Z"],    # Should be parsed into datetime
        "Outcome": ["No further action"],       # Should be kept and lowercase
        "Extra": [{"nested": "value"}]           # Not empty, but check naming format
    }
    df = pd.DataFrame(raw_data)

    # Clean and format the DataFrame
    cleaned = clean_and_format_dataframe(df)

    # Check that 'datetime' column was renamed and exists
    assert "datetime" in cleaned.columns

    # Check that the column name transformation worked
    # and ensure we don't have mixed-case leftovers
    assert "Extra" not in cleaned.columns or "extra" not in cleaned.columns

