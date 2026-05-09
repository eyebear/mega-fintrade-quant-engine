from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.adapters import (
    read_cleaned_market_data,
    read_daily_returns,
    prepare_backtest_dataframe,
    convert_to_price_matrix,
)
from src.backtester import Backtester
from src.config import (
    CLEANED_MARKET_DATA_PATH,
    DAILY_RETURNS_PATH,
    STRATEGY_SIGNALS_PATH,
    BACKTEST_RESULTS_PATH,
    RISK_METRICS_PATH,
    PORTFOLIO_EQUITY_CURVE_PATH,
)
from src.metrics import summarize_metrics
from src.portfolio import EqualWeightAllocator
from src.strategies import MovingAverageCrossStrategy


BACKEND_STRATEGY_SYMBOL_ORDER = ["AAPL", "MSFT", "GOOGL", "SPY"]


def ensure_output_directory() -> None:
    Path("data/output").mkdir(parents=True, exist_ok=True)


def export_strategy_signals(signals: pd.DataFrame, output_path: str) -> None:
    flat_signals = signals.copy()

    if isinstance(flat_signals.columns, pd.MultiIndex):
        flat_signals.columns = [
            f"{asset}_{field}" for asset, field in flat_signals.columns
        ]

    flat_signals = flat_signals.reset_index()

    if "index" in flat_signals.columns and "date" not in flat_signals.columns:
        flat_signals = flat_signals.rename(columns={"index": "date"})

    if "Date" in flat_signals.columns and "date" not in flat_signals.columns:
        flat_signals = flat_signals.rename(columns={"Date": "date"})

    rename_map: dict[str, str] = {}

    for symbol in BACKEND_STRATEGY_SYMBOL_ORDER:
        lower_symbol = symbol.lower()

        rename_map[f"{symbol}_close"] = f"{lower_symbol}_close"
        rename_map[f"{symbol}_short_ma"] = f"{lower_symbol}_sma_short"
        rename_map[f"{symbol}_long_ma"] = f"{lower_symbol}_sma_long"
        rename_map[f"{symbol}_signal"] = f"{lower_symbol}_signal"

        rename_map[f"{symbol}_sma_short"] = f"{lower_symbol}_sma_short"
        rename_map[f"{symbol}_sma_long"] = f"{lower_symbol}_sma_long"

        rename_map[f"{lower_symbol}_close"] = f"{lower_symbol}_close"
        rename_map[f"{lower_symbol}_short_ma"] = f"{lower_symbol}_sma_short"
        rename_map[f"{lower_symbol}_long_ma"] = f"{lower_symbol}_sma_long"
        rename_map[f"{lower_symbol}_signal"] = f"{lower_symbol}_signal"

    flat_signals = flat_signals.rename(columns=rename_map)

    expected_columns = ["date"]

    for symbol in BACKEND_STRATEGY_SYMBOL_ORDER:
        lower_symbol = symbol.lower()
        expected_columns.extend(
            [
                f"{lower_symbol}_close",
                f"{lower_symbol}_sma_short",
                f"{lower_symbol}_sma_long",
                f"{lower_symbol}_signal",
            ]
        )

    missing_columns = [
        column for column in expected_columns if column not in flat_signals.columns
    ]

    if missing_columns:
        raise ValueError(
            "strategy_signals.csv is missing required backend columns: "
            + ", ".join(missing_columns)
        )

    backend_signals = flat_signals[expected_columns].copy()

    numeric_columns = [column for column in expected_columns if column != "date"]

    for column in numeric_columns:
        backend_signals[column] = pd.to_numeric(backend_signals[column], errors="coerce")

    before_drop_count = len(backend_signals)

    backend_signals = backend_signals.dropna(subset=numeric_columns)

    after_drop_count = len(backend_signals)
    dropped_count = before_drop_count - after_drop_count

    if backend_signals.empty:
        raise ValueError(
            "strategy_signals.csv has no complete rows after removing rows with missing moving average values."
        )

    backend_signals.to_csv(output_path, index=False)

    print(
        "Prepared backend-compatible strategy signals. "
        f"Dropped {dropped_count} rows with incomplete moving average values."
    )


def export_backtest_results(detail: pd.DataFrame, output_path: str) -> None:
    detail.to_csv(output_path, index=True)


def export_portfolio_equity_curve(detail: pd.DataFrame, output_path: str) -> None:
    equity_curve = detail[
        [
            "portfolio_wealth",
            "benchmark_wealth",
        ]
    ].copy()

    equity_curve.to_csv(output_path, index=True)


def build_asset_risk_metrics(daily_returns: pd.DataFrame) -> pd.DataFrame:
    required_columns = ["symbol", "date", "daily_return"]

    for column in required_columns:
        if column not in daily_returns.columns:
            raise ValueError(f"Missing required column in daily returns file: {column}")

    rows: list[dict[str, object]] = []

    for symbol, group in daily_returns.groupby("symbol"):
        returns = group.sort_values("date")["daily_return"]
        summary = summarize_metrics(returns)

        for metric, value in summary.items():
            rows.append(
                {
                    "scope": "asset",
                    "symbol": symbol,
                    "metric": metric,
                    "value": value,
                }
            )

    return pd.DataFrame(rows)


def build_portfolio_risk_metrics(result_summary: pd.Series) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    for metric, value in result_summary.items():
        rows.append(
            {
                "scope": "portfolio",
                "symbol": "ALL",
                "metric": metric,
                "value": value,
            }
        )

    return pd.DataFrame(rows)


def export_risk_metrics(
    portfolio_summary: pd.Series,
    daily_returns: pd.DataFrame,
    output_path: str,
) -> None:
    portfolio_metrics = build_portfolio_risk_metrics(portfolio_summary)
    asset_metrics = build_asset_risk_metrics(daily_returns)

    risk_metrics = pd.concat(
        [portfolio_metrics, asset_metrics],
        ignore_index=True,
    )

    risk_metrics.to_csv(output_path, index=False)


def main() -> None:
    ensure_output_directory()

    cleaned_market_data = read_cleaned_market_data(CLEANED_MARKET_DATA_PATH)
    daily_returns = read_daily_returns(DAILY_RETURNS_PATH)

    backtest_data = prepare_backtest_dataframe(cleaned_market_data)
    price_matrix = convert_to_price_matrix(backtest_data)

    strategy = MovingAverageCrossStrategy(
        short_window=20,
        long_window=50,
    )

    allocator = EqualWeightAllocator()

    backtester = Backtester(
        strategy=strategy,
        allocator=allocator,
        transaction_cost_bps=5.0,
        benchmark="SPY" if "SPY" in price_matrix.columns else None,
    )

    result = backtester.run(price_matrix)

    signals = strategy.generate_signals(price_matrix)

    export_strategy_signals(signals, STRATEGY_SIGNALS_PATH)
    export_backtest_results(result.detail, BACKTEST_RESULTS_PATH)
    export_risk_metrics(result.summary, daily_returns, RISK_METRICS_PATH)
    export_portfolio_equity_curve(result.detail, PORTFOLIO_EQUITY_CURVE_PATH)

    print("Project 2 analytics pipeline completed successfully.")
    print(f"Read cleaned market data input: {CLEANED_MARKET_DATA_PATH}")
    print(f"Read daily returns input: {DAILY_RETURNS_PATH}")
    print(f"Wrote strategy signals: {STRATEGY_SIGNALS_PATH}")
    print(f"Wrote backtest results: {BACKTEST_RESULTS_PATH}")
    print(f"Wrote risk metrics: {RISK_METRICS_PATH}")
    print(f"Wrote portfolio equity curve: {PORTFOLIO_EQUITY_CURVE_PATH}")


if __name__ == "__main__":
    main()