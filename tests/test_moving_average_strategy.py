import pandas as pd

from src.strategies import MovingAverageCrossStrategy


def test_moving_average_strategy_generates_signal():
    prices = pd.DataFrame({
        "AAPL": [100.0, 101.0, 102.0]
    })

    strategy = MovingAverageCrossStrategy(short_window=1, long_window=2)
    signals = strategy.generate_signals(prices)

    assert ("AAPL", "signal") in signals.columns
    assert signals[("AAPL", "signal")].iloc[0] == 0.0
    assert signals[("AAPL", "signal")].iloc[1] == 1.0
    assert signals[("AAPL", "signal")].iloc[2] == 1.0