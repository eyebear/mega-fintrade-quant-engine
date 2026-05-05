## Integration with mega-fintrade-market-engine-cpp

The `mega-fintrade-quant-engine` repository integrates with the C++ market data processing engine from `mega-fintrade-market-engine-cpp`.

The `mega-fintrade-market-engine-cpp` repository is responsible for cleaning raw market data and calculating daily returns. The `mega-fintrade-quant-engine` repository consumes those C++ output files and uses them for strategy generation, backtesting, portfolio equity curve generation, and risk analytics.

### Integration Data Flow

The `mega-fintrade-quant-engine` repository downloads and normalizes raw market data:

    data/raw/raw_market_data.csv

The `mega-fintrade-market-engine-cpp` repository processes the raw market data and produces:

    data/output/cleaned_market_data.csv
    data/output/daily_returns.csv

Those files are copied into `mega-fintrade-quant-engine`:

    data/processed/cleaned_market_data.csv
    data/processed/daily_returns.csv

The `mega-fintrade-quant-engine` analytics pipeline then produces:

    data/output/strategy_signals.csv
    data/output/backtest_results.csv
    data/output/risk_metrics.csv
    data/output/portfolio_equity_curve.csv

### C++ Output Files Used by mega-fintrade-quant-engine

| File | Source Repository | Destination in mega-fintrade-quant-engine | Purpose |
|---|---|---|---|
| `cleaned_market_data.csv` | `mega-fintrade-market-engine-cpp` | `data/processed/cleaned_market_data.csv` | Used to build the price matrix for strategy signals, backtesting, and portfolio equity curve generation |
| `daily_returns.csv` | `mega-fintrade-market-engine-cpp` | `data/processed/daily_returns.csv` | Used to calculate asset-level risk metrics |

### Expected Input Schemas

`cleaned_market_data.csv` must use this schema:

    symbol,date,open,high,low,close,volume

`daily_returns.csv` must use this schema:

    symbol,date,previous_close,current_close,daily_return

### Running the Integrated Analytics Pipeline

After copying the output files from `mega-fintrade-market-engine-cpp` into `mega-fintrade-quant-engine/data/processed`, run:

    python3 -m src.run_pipeline

This command reads:

    data/processed/cleaned_market_data.csv
    data/processed/daily_returns.csv

and regenerates:

    data/output/strategy_signals.csv
    data/output/backtest_results.csv
    data/output/risk_metrics.csv
    data/output/portfolio_equity_curve.csv

### Validating the Integration

Run the full test suite:

    python3 -m pytest

Expected result:

    14 passed

Then validate the generated output files:

    ls -l data/output
    head -5 data/output/risk_metrics.csv

The `risk_metrics.csv` file should contain both portfolio-level and asset-level metrics, for example:

    portfolio,ALL,cumulative_return,...
    asset,AAPL,cumulative_return,...

This confirms that `mega-fintrade-quant-engine` is using both C++ output files from `mega-fintrade-market-engine-cpp`:

- `cleaned_market_data.csv` for strategy and backtest generation
- `daily_returns.csv` for asset-level risk metrics