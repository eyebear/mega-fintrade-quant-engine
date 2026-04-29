from __future__ import annotations

import pandas as pd


def simulate_integer_shares(
    prices: pd.DataFrame,
    weights: pd.DataFrame,
    initial_cash: float = 100000.0
) -> pd.DataFrame:
    prices = prices.sort_index()
    weights = weights.reindex(prices.index).fillna(0.0)

    records = []
    cash = initial_cash
    shares = pd.Series(0, index=prices.columns, dtype=int)

    for date in prices.index:
        current_prices = prices.loc[date]
        portfolio_value = cash + (shares * current_prices).sum()

        target_values = portfolio_value * weights.loc[date]
        target_shares = (target_values / current_prices).fillna(0).astype(int)

        trade_shares = target_shares - shares
        trade_value = (trade_shares * current_prices).sum()

        cash -= trade_value
        shares = target_shares

        equity = cash + (shares * current_prices).sum()

        record = {
            "date": date,
            "cash": cash,
            "equity": equity
        }

        for symbol in prices.columns:
            record[f"{symbol}_shares"] = shares[symbol]

        records.append(record)

    return pd.DataFrame(records).set_index("date")