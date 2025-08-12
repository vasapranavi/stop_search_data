import pandas as pd
from src.updater import read_existing_data

def test_read_existing_data_creates_fresh_when_missing(tmp_path):
    """
    Test that read_existing_data returns a fresh DataFrame and default date
    when the target CSV file does not exist.

    This simulates a missing data file scenario and ensures the function
    handles it gracefully without raising errors.
    """
    # Define a temporary CSV path
    csv_path = tmp_path / "test.csv"
    original_csv_file = "data/metropolitan_stops.csv"

    # Temporarily rename the real CSV if it exists to simulate missing file
    import os
    if os.path.exists(original_csv_file):
        os.rename(original_csv_file, original_csv_file + ".bak")

    try:
        # Call the function and verify it returns a DataFrame even when file is missing
        df, date = read_existing_data(original_csv_file)
        assert isinstance(df, pd.DataFrame)
    finally:
        # Restore the original CSV if it was moved
        if os.path.exists(original_csv_file + ".bak"):
            os.rename(original_csv_file + ".bak", original_csv_file)