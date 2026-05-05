import pandas as pd

CLEANED_MARKET_DATA_COLUMNS = ["symbol", "date", "open", "high", "low", "close", "volume"]
DAILY_RETURNS_COLUMNS = ["symbol", "date", "previous_close", "current_close", "daily_return"]

def read_cleaned_market_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    validate_schema(df, CLEANED_MARKET_DATA_COLUMNS)
    return df


def read_daily_returns(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    validate_schema(df, DAILY_RETURNS_COLUMNS)
    return df

def validate_schema(df: pd.DataFrame, expected_columns: list[str]) -> None:
    actual_columns = list(df.columns)

    if actual_columns != expected_columns:
        raise ValueError(
            f"Invalid schema. Expected {expected_columns}, got {actual_columns}"
        )
    
def prepare_backtest_dataframe(cleaned_market_data: pd.DataFrame) -> pd.DataFrame:
    df = cleaned_market_data.copy()

    validate_schema(df, CLEANED_MARKET_DATA_COLUMNS)

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values(["symbol", "date"]).reset_index(drop=True)

    return df

def convert_to_price_matrix(backtest_data: pd.DataFrame) -> pd.DataFrame:
    df = backtest_data.copy()

    required_columns = ["symbol", "date", "close"]
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    df["date"] = pd.to_datetime(df["date"])

    price_matrix = df.pivot(
        index="date",
        columns="symbol",
        values="close"
    ).sort_index()

    return price_matrix