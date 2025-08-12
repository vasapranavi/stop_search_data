import pytest
from src.fetcher import fetch_data_for_month

def test_fetch_valid_month():
    """
    Test that fetch_data_for_month returns a list for valid inputs.

    This test verifies that calling the function with a valid police force ID,
    year, and month returns a result of type list (even if it's empty).
    """
    # Call the function with known valid parameters
    data = fetch_data_for_month("metropolitan", 2024, 1)

    # Verify that the returned value is a list
    assert isinstance(data, list)


def test_fetch_invalid_force():
    """
    Test that fetch_data_for_month returns an empty list for an invalid force ID.

    This ensures the function handles API errors or invalid parameters gracefully
    by returning an empty list instead of raising an exception.
    """
    # Call the function with an invalid police force ID
    data = fetch_data_for_month("invalid-force-id", 2024, 1)

    # Expect an empty list as no data should be returned for an invalid force
    assert data == []