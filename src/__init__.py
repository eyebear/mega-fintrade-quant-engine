"""QuantFolio Showcase package."""

from .backtester import BacktestResult, Backtester
from .data import load_price_csv, make_demo_prices
from .factor_momentum import TopNMomentumStrategy
from .metrics import summarize_metrics
from .multi_factor import MultiFactorStrategy
from .portfolio import EqualWeightAllocator
from .strategies import MovingAverageCrossStrategy, RelativeStrengthStrategy

__all__ = [
    "BacktestResult",
    "Backtester",
    "EqualWeightAllocator",
    "MultiFactorStrategy",
    "TopNMomentumStrategy",
    "MovingAverageCrossStrategy",
    "RelativeStrengthStrategy",
    "load_price_csv",
    "make_demo_prices",
    "summarize_metrics",
]
