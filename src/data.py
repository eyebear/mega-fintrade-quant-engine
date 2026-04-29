from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


def load_price_csv(path: str | Path) -> pd.DataFrame:
    """Load a wide price table from CSV.

    Expected format:
    - a `date` column
    - one column per asset containing close prices
    """
    df = pd.read_csv(path, parse_dates=["date"])
    df = df.set_index("date").sort_index()
    if df.empty:
        raise ValueError("price table is empty")
    if df.isna().all().all():
        raise ValueError("price table contains only missing values")
    return df.astype(float)


def make_demo_prices(
    periods: int = 756,
    assets: tuple[str, ...] = ("SPY", "QQQ", "TLT", "GLD", "XLF"),
    seed: int = 42,
) -> pd.DataFrame:
    """Create deterministic synthetic daily prices for demonstration."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2021-01-01", periods=periods)

    series: dict[str, pd.Series] = {}
    for i, asset in enumerate(assets):
        drift = 0.0002 + (i * 0.00005)
        vol = 0.008 + (i * 0.001)
        shocks = rng.normal(loc=drift, scale=vol, size=periods)
        prices = 100.0 * np.exp(np.cumsum(shocks))
        series[asset] = pd.Series(prices, index=dates)

    return pd.DataFrame(series)
