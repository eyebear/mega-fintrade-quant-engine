from __future__ import annotations

import os
import pandas as pd


def export_strategy_signals(
    signals: pd.DataFrame,
    output_path: str = "data/output/strategy_signals.csv"
) -> pd.DataFrame:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    flat = signals.copy()

    if isinstance(flat.columns, pd.MultiIndex):
        flat.columns = [f"{asset}_{field}" for asset, field in flat.columns]

    flat = flat.reset_index()

    flat.to_csv(output_path, index=False)

    return flat

def export_backtest_results(
    results: pd.DataFrame,
    output_path: str = "data/output/backtest_results.csv"
) -> pd.DataFrame:
    import os

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = results.copy().reset_index()

    df.to_csv(output_path, index=False)

    return df

def export_risk_metrics(
    metrics: pd.Series,
    output_path: str = "data/output/risk_metrics.csv"
) -> pd.DataFrame:
    import os

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = metrics.to_frame(name="value").reset_index()
    df.columns = ["metric", "value"]

    df.to_csv(output_path, index=False)

    return df

def export_equity_curve(
    results: pd.DataFrame,
    output_path: str = "data/output/portfolio_equity_curve.csv"
) -> pd.DataFrame:
    import os

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = results[["equity"]].copy().reset_index()

    df.to_csv(output_path, index=False)

    return df