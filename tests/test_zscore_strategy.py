import pandas as pd

from src.strategies import ZScoreStrategy


def test_zscore_strategy_generates_signal_columns():
    prices = pd.DataFrame({
        "AAPL": [100.0, 101.0, 102.0, 90.0]
    })

    strategy = ZScoreStrategy(
        lookback=3,
        entry_threshold=-0.5,
        exit_threshold=0.5
    )

    signals = strategy.generate_signals(prices)

    assert ("AAPL", "close") in signals.columns
    assert ("AAPL", "zscore") in signals.columns
    assert ("AAPL", "signal") in signals.columns