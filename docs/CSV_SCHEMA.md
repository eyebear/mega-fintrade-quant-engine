# Mega Fintrade — CSV Schema Documentation

## 1. strategy_signals.csv

Columns:
- date (string, YYYY-MM-DD)
- {SYMBOL}_close (float)
- {SYMBOL}_short_ma (float)
- {SYMBOL}_long_ma (float)
- {SYMBOL}_signal (float)

Example:
date,AAPL_close,AAPL_short_ma,AAPL_long_ma,AAPL_signal

---

## 2. backtest_results.csv

Columns:
- date
- gross_portfolio_return (float)
- transaction_cost_rate (float)
- net_portfolio_return (float)
- equity (float)

---

## 3. risk_metrics.csv

Columns:
- metric (string)
- value (float)

Metrics:
- cumulative_return
- cagr
- annualized_volatility
- sharpe_ratio
- max_drawdown
- hit_rate

---

## 4. portfolio_equity_curve.csv

Columns:
- date
- equity (float)