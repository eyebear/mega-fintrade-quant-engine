import yfinance as yf
import pandas as pd
import os
from src.config import DEFAULT_TICKERS, START_DATE, END_DATE, RAW_MARKET_DATA_PATH

from src.config import DEFAULT_TICKERS, START_DATE, END_DATE


def download_market_data(
    tickers=None,
    start_date: str = START_DATE,
    end_date: str = END_DATE
) -> pd.DataFrame:
    if tickers is None:
        tickers = DEFAULT_TICKERS

    frames = []

    for symbol in tickers:
        data = yf.download(
            symbol,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=False
        )

        if data.empty:
            continue

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data = data.reset_index()
        data["symbol"] = symbol
        frames.append(data)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)

def normalize_market_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    if raw_data.empty:
        return pd.DataFrame(
            columns=["symbol", "date", "open", "high", "low", "close", "volume"]
        )

    normalized = raw_data.rename(
        columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
    )

    normalized = normalized[
        ["symbol", "date", "open", "high", "low", "close", "volume"]
    ]

    normalized["date"] = pd.to_datetime(normalized["date"]).dt.strftime("%Y-%m-%d")

    return normalized

def export_raw_market_data(output_path: str = RAW_MARKET_DATA_PATH) -> pd.DataFrame:
    raw_data = download_market_data()
    normalized_data = normalize_market_data(raw_data)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    normalized_data.to_csv(output_path, index=False)

    return normalized_data