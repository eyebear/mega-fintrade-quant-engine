from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

from .metrics import summarize_metrics
from .portfolio import EqualWeightAllocator
from .strategies import Strategy


@dataclass
class BacktestResult:
    portfolio_returns: pd.Series
    benchmark_returns: pd.Series
    weights: pd.DataFrame
    turnover: pd.Series
    summary: pd.Series
    detail: pd.DataFrame


@dataclass
class Backtester:
    strategy: Strategy
    allocator: EqualWeightAllocator
    transaction_cost_bps: float = 5.0
    benchmark: str | None = None

    def run(self, prices: pd.DataFrame) -> BacktestResult:
        """Run a daily close-to-close multi-asset backtest.

        Signals are lagged by one day to avoid look-ahead bias.
        Transaction costs are applied on daily turnover.
        """
        if prices.empty:
            raise ValueError("prices cannot be empty")

        signal_output = self.strategy.generate_signals(prices)
        if isinstance(signal_output.columns, pd.MultiIndex):
            signal_frame = signal_output.xs("signal", axis=1, level=1)
        else:
            signal_frame = signal_output.copy()

        weights = self.allocator.allocate(signal_frame).shift(1).fillna(0.0)

        asset_returns = prices.pct_change().fillna(0.0)
        gross_returns = (weights * asset_returns).sum(axis=1)

        turnover = weights.diff().abs().sum(axis=1).fillna(weights.abs().sum(axis=1))
        transaction_cost_rate = self.transaction_cost_bps / 10000.0
        net_returns = gross_returns - (turnover * transaction_cost_rate)

        benchmark_col = self.benchmark or prices.columns[0]
        benchmark_returns = asset_returns[benchmark_col]

        summary = summarize_metrics(net_returns, average_turnover=float(turnover.mean()))

        detail = pd.DataFrame(
            {
                "portfolio_return": net_returns,
                "benchmark_return": benchmark_returns,
                "turnover": turnover,
            },
            index=prices.index,
        )
        detail["portfolio_wealth"] = (1.0 + detail["portfolio_return"]).cumprod()
        detail["benchmark_wealth"] = (1.0 + detail["benchmark_return"]).cumprod()

        return BacktestResult(
            portfolio_returns=net_returns,
            benchmark_returns=benchmark_returns,
            weights=weights,
            turnover=turnover,
            summary=summary,
            detail=detail,
        )
