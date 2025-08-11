import pytest
from src.fetcher import fetch_data_for_month

def test_fetch_valid_month():
    data = fetch_data_for_month("metropolitan", 2024, 1)
    assert isinstance(data, list)

def test_fetch_invalid_force():
    data = fetch_data_for_month("invalid-force-id", 2024, 1)
    assert data == []