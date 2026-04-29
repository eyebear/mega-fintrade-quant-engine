import pandas as pd
from src.ingestion import normalize_market_data


def test_normalize_market_data_basic():
    raw = pd.DataFrame({
        "Date": ["2024-01-01", "2024-01-02"],
        "Open": [100, 110],
        "High": [105, 115],
        "Low": [95, 108],
        "Close": [102, 112],
        "Volume": [1000, 2000],
        "symbol": ["AAPL", "AAPL"]
    })

    df = normalize_market_data(raw)

    assert list(df.columns) == [
        "symbol", "date", "open", "high", "low", "close", "volume"
    ]

    assert df.iloc[0]["symbol"] == "AAPL"
    assert df.iloc[0]["date"] == "2024-01-01"
    assert df.iloc[0]["open"] == 100