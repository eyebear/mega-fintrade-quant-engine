from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt

from .backtester import BacktestResult


def save_performance_chart(result: BacktestResult, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.plot(result.detail.index, result.detail["portfolio_wealth"], label="Portfolio")
    plt.plot(result.detail.index, result.detail["benchmark_wealth"], label="Benchmark")
    plt.title("Portfolio vs Benchmark")
    plt.xlabel("Date")
    plt.ylabel("Growth of 1")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path


def save_markdown_report(result: BacktestResult, output_path: str | Path, strategy_name: str) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# QuantFolio Backtest Report",
        "",
        f"**Strategy:** {strategy_name}",
        "",
        "## Summary Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]

    for key, value in result.summary.items():
        lines.append(f"| {key} | {value:.4f} |")

    lines.extend(
        [
            "",
            "## Final Portfolio Weights",
            "",
            result.weights.tail(1).to_markdown(),
            "",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path
