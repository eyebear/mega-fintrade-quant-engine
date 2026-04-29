from __future__ import annotations

import argparse
from pathlib import Path

from .backtester import Backtester
from .data import load_price_csv, make_demo_prices
from .portfolio import EqualWeightAllocator
from .report import save_markdown_report, save_performance_chart
from .strategies import MovingAverageCrossStrategy, RelativeStrengthStrategy


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="QuantFolio Showcase CLI")
    parser.add_argument("--csv", type=str, help="Path to a wide price CSV file")
    parser.add_argument("--demo", action="store_true", help="Use built-in demo data")
    parser.add_argument("--strategy", choices=["ma", "momentum"], default="ma")
    parser.add_argument("--short-window", type=int, default=20)
    parser.add_argument("--long-window", type=int, default=50)
    parser.add_argument("--lookback", type=int, default=60)
    parser.add_argument("--top-n", type=int, default=2)
    parser.add_argument("--transaction-cost-bps", type=float, default=5.0)
    parser.add_argument("--benchmark", type=str, default=None)
    parser.add_argument("--output-dir", type=str, default="outputs")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.demo and not args.csv:
        parser.error("Provide either --demo or --csv")

    prices = make_demo_prices() if args.demo else load_price_csv(args.csv)

    if args.strategy == "ma":
        strategy = MovingAverageCrossStrategy(
            short_window=args.short_window,
            long_window=args.long_window,
        )
        strategy_name = f"MovingAverageCross({args.short_window}, {args.long_window})"
    else:
        strategy = RelativeStrengthStrategy(
            lookback=args.lookback,
            top_n=args.top_n,
        )
        strategy_name = f"RelativeStrength(lookback={args.lookback}, top_n={args.top_n})"

    allocator = EqualWeightAllocator()
    backtester = Backtester(
        strategy=strategy,
        allocator=allocator,
        transaction_cost_bps=args.transaction_cost_bps,
        benchmark=args.benchmark,
    )

    result = backtester.run(prices)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    chart_path = save_performance_chart(result, output_dir / "performance.png")
    report_path = save_markdown_report(result, output_dir / "report.md", strategy_name)

    print("Backtest complete")
    print(result.summary.to_string())
    print(f"Chart saved to: {chart_path}")
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
