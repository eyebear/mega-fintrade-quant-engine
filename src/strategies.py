from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
import numpy as np
import pandas as pd


class Strategy(Protocol):
    def generate_signals(self, prices: pd.DataFrame) -> pd.DataFrame:
        ...


@dataclass
class MovingAverageCrossStrategy:
    short_window: int = 20
    long_window: int = 50

    def generate_signals(self, prices: pd.DataFrame) -> pd.DataFrame:
        """Generate long-only binary signals for each asset.

        Signal is 1.0 when short moving average is above long moving average,
        otherwise 0.0.
        """
        if self.short_window >= self.long_window:
            raise ValueError("short_window must be less than long_window")

        frames: list[pd.DataFrame] = []
        for asset in prices.columns:
            close = prices[asset]
            short_ma = close.rolling(self.short_window, min_periods=self.short_window).mean()
            long_ma = close.rolling(self.long_window, min_periods=self.long_window).mean()
            signal = np.where(short_ma > long_ma, 1.0, 0.0)
            asset_frame = pd.DataFrame(
                {
                    (asset, "close"): close,
                    (asset, "short_ma"): short_ma,
                    (asset, "long_ma"): long_ma,
                    (asset, "signal"): pd.Series(signal, index=prices.index).fillna(0.0),
                }
            )
            frames.append(asset_frame)

        return pd.concat(frames, axis=1)


@dataclass
class RelativeStrengthStrategy:
    lookback: int = 60
    top_n: int = 2

    def generate_signals(self, prices: pd.DataFrame) -> pd.DataFrame:
        """Allocate to the strongest assets based on trailing returns.

        For each day, signal is 1.0 for the top_n assets ranked by trailing return
        over the lookback window, and 0.0 for all others.
        """
        if self.top_n <= 0:
            raise ValueError("top_n must be positive")
        if self.top_n > len(prices.columns):
            raise ValueError("top_n cannot exceed number of assets")

        trailing_return = prices / prices.shift(self.lookback) - 1.0
        signal = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)

        valid_rows = trailing_return.dropna(how="all")
        for dt, row in valid_rows.iterrows():
            winners = row.nlargest(self.top_n).index
            signal.loc[dt, winners] = 1.0

        frames: list[pd.DataFrame] = []
        for asset in prices.columns:
            asset_frame = pd.DataFrame(
                {
                    (asset, "close"): prices[asset],
                    (asset, "trailing_return"): trailing_return[asset],
                    (asset, "signal"): signal[asset],
                }
            )
            frames.append(asset_frame)

        return pd.concat(frames, axis=1)

@dataclass
class ZScoreStrategy:
    lookback: int = 20
    entry_threshold: float = -1.0
    exit_threshold: float = 0.0

    def calculate_rolling_mean(self, prices: pd.DataFrame) -> pd.DataFrame:
        return prices.rolling(
            window=self.lookback,
            min_periods=self.lookback
        ).mean()