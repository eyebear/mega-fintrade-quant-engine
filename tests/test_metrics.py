from __future__ import annotations

import pandas as pd

from src.metrics import cumulative_returns, max_drawdown, summarize_metrics


def test_cumulative_returns_starts_at_one_plus_first_return() -> None:
    returns = pd.Series([0.10, -0.05])
    wealth = cumulative_returns(returns)
    assert round(float(wealth.iloc[0]), 4) == 1.1000
    assert round(float(wealth.iloc[1]), 4) == 1.0450


def test_max_drawdown_is_negative_after_loss() -> None:
    returns = pd.Series([0.10, -0.20, 0.05])
    drawdown = max_drawdown(returns)
    assert round(drawdown, 4) == -0.2000


def test_summarize_metrics_contains_expected_fields() -> None:
    returns = pd.Series([0.01, -0.02, 0.03, 0.00])
    summary = summarize_metrics(returns, average_turnover=0.25)
    assert "cagr" in summary.index
    assert "sharpe_ratio" in summary.index
    assert "average_daily_turnover" in summary.index
