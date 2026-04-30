import pandas as pd

from src.exports import (
    export_strategy_signals,
    export_backtest_results,
    export_risk_metrics,
    export_equity_curve,
)


def test_export_strategy_signals(tmp_path):
    signals = pd.DataFrame({
        ("AAPL", "close"): [100.0],
        ("AAPL", "signal"): [1.0],
    }, index=pd.Index(["2024-01-01"], name="date"))

    output = tmp_path / "strategy_signals.csv"
    df = export_strategy_signals(signals, str(output))

    assert output.exists()
    assert "AAPL_close" in df.columns
    assert "AAPL_signal" in df.columns


def test_export_backtest_results(tmp_path):
    results = pd.DataFrame({
        "gross_portfolio_return": [0.0],
        "transaction_cost_rate": [0.0],
        "net_portfolio_return": [0.0],
        "equity": [100000.0],
    }, index=pd.Index(["2024-01-01"], name="date"))

    output = tmp_path / "backtest_results.csv"
    df = export_backtest_results(results, str(output))

    assert output.exists()
    assert "equity" in df.columns


def test_export_risk_metrics(tmp_path):
    metrics = pd.Series({
        "cumulative_return": 0.1,
        "sharpe_ratio": 1.0,
    })

    output = tmp_path / "risk_metrics.csv"
    df = export_risk_metrics(metrics, str(output))

    assert output.exists()
    assert "metric" in df.columns
    assert "value" in df.columns


def test_export_equity_curve(tmp_path):
    results = pd.DataFrame({
        "equity": [100000.0, 101000.0]
    }, index=pd.Index(["2024-01-01", "2024-01-02"], name="date"))

    output = tmp_path / "equity_curve.csv"
    df = export_equity_curve(results, str(output))

    assert output.exists()
    assert "equity" in df.columns