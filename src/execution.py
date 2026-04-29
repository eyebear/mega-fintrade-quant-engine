from __future__ import annotations

import pandas as pd



def run_close_to_close_backtest(
    prices: pd.DataFrame,
    weights: pd.DataFrame,
    initial_cash: float = 100000.0,
    commission_rate: float = 0.001,
    slippage_rate: float = 0.0005
) -> pd.DataFrame:
    prices = prices.sort_index()
    weights = weights.reindex(prices.index).fillna(0.0)

    returns = prices.pct_change().fillna(0.0)

    shifted_weights = weights.shift(1).fillna(0.0)

    gross_portfolio_returns = (shifted_weights * returns).sum(axis=1)

    weight_changes = weights.diff().abs().sum(axis=1).fillna(0.0)

    transaction_cost_rate = weight_changes * (commission_rate + slippage_rate)

    net_portfolio_returns = gross_portfolio_returns - transaction_cost_rate

    equity = initial_cash * (1.0 + net_portfolio_returns).cumprod()

    result = pd.DataFrame({
        "gross_portfolio_return": gross_portfolio_returns,
        "transaction_cost_rate": transaction_cost_rate,
        "net_portfolio_return": net_portfolio_returns,
        "equity": equity
    })

    return result