import pandas as pd

from src.ingestion import normalize_market_data


def test_normalize_market_data_schema():
    raw = pd.DataFrame({
        "Date": ["2024-01-01"],
        "Open": [100.0],
        "High": [105.0],
        "Low": [99.0],
        "Close": [103.0],
        "Volume": [1000000],
        "symbol": ["AAPL"],
    })

    result = normalize_market_data(raw)

    assert list(result.columns) == [
        "symbol",
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]