import pandas as pd

from src.metrics import (
    cumulative_returns,
    annualized_volatility,
    sharpe_ratio,
    max_drawdown,
    hit_rate,
    summarize_metrics,
)


def test_performance_metrics_summary_contains_expected_fields():
    returns = pd.Series([0.01, -0.02, 0.03, 0.0])

    summary = summarize_metrics(returns)

    assert "cumulative_return" in summary.index
    assert "cagr" in summary.index
    assert "annualized_volatility" in summary.index
    assert "sharpe_ratio" in summary.index
    assert "max_drawdown" in summary.index
    assert "hit_rate" in summary.index


def test_hit_rate_ignores_zero_returns():
    returns = pd.Series([0.01, -0.02, 0.03, 0.0])

    assert hit_rate(returns) == 2 / 3


def test_cumulative_returns_final_value():
    returns = pd.Series([0.05, 0.0476190476])

    result = cumulative_returns(returns)

    assert round(result.iloc[-1], 6) == 1.1