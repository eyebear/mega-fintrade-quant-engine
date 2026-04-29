from __future__ import annotations

from pathlib import Path

from src.quantfolio_showcase import MultiFactorStrategy
from src.quantfolio_showcase.backtester import Backtester
from src.quantfolio_showcase.data import make_demo_prices
from src.quantfolio_showcase.factor_momentum import TopNMomentumStrategy
from src.quantfolio_showcase.portfolio import EqualWeightAllocator
from src.quantfolio_showcase.report import save_markdown_report, save_performance_chart
from src.quantfolio_showcase.strategies import MovingAverageCrossStrategy
from pathlib import Path
from src.quantfolio_showcase.data_loader import load_price_data

def main() -> None:


    symbols = ["AAPL", "MSFT", "GOOGL", "SPY"]

    prices = load_price_data(
        symbols=symbols,
        start="2020-01-01",
        end="2024-01-01",
        data_dir=Path("data")
    )
    #prices = make_demo_prices()
    #strategy = MovingAverageCrossStrategy(short_window=20, long_window=50)
    #strategy = TopNMomentumStrategy(lookback=60, top_n=2)
    strategy = MultiFactorStrategy(
        momentum_lookback=60,
        volatility_lookback=20,
        reversal_lookback=5,
        top_n=2,
        momentum_weight=0.5,
        low_vol_weight=0.3,
        reversal_weight=0.2,
    )
    allocator = EqualWeightAllocator()
    result = Backtester(strategy=strategy, allocator=allocator, benchmark="SPY").run(prices)

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    save_performance_chart(result, output_dir / "demo_performance.png")
    save_markdown_report(result, output_dir / "demo_report.md", "MovingAverageCross(20, 50)")

    print(result.summary.to_string())


if __name__ == "__main__":
    main()
