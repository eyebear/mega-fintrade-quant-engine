from __future__ import annotations

import math
import pandas as pd


TRADING_DAYS_PER_YEAR = 252


def cumulative_returns(returns: pd.Series) -> pd.Series:
    return (1.0 + returns).cumprod()


def cagr(returns: pd.Series) -> float:
    if returns.empty:
        return 0.0
    wealth = cumulative_returns(returns)
    years = len(returns) / TRADING_DAYS_PER_YEAR
    if years <= 0:
        return 0.0
    return float((wealth.iloc[-1] ** (1.0 / years)) - 1.0)


def annualized_volatility(returns: pd.Series) -> float:
    if len(returns) < 2:
        return 0.0
    return float(returns.std(ddof=1) * math.sqrt(TRADING_DAYS_PER_YEAR))


def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    if len(returns) < 2:
        return 0.0
    daily_rf = risk_free_rate / TRADING_DAYS_PER_YEAR
    excess = returns - daily_rf
    vol = excess.std(ddof=1)
    if vol == 0:
        return 0.0
    return float((excess.mean() / vol) * math.sqrt(TRADING_DAYS_PER_YEAR))


def max_drawdown(returns: pd.Series) -> float:
    wealth = cumulative_returns(returns)
    running_max = wealth.cummax()
    drawdown = wealth / running_max - 1.0
    return float(drawdown.min()) if not drawdown.empty else 0.0


def summarize_metrics(returns: pd.Series, average_turnover: float | None = None) -> pd.Series:
    summary = {
        "cumulative_return": float(cumulative_returns(returns).iloc[-1] - 1.0) if not returns.empty else 0.0,
        "cagr": cagr(returns),
        "annualized_volatility": annualized_volatility(returns),
        "sharpe_ratio": sharpe_ratio(returns),
        "max_drawdown": max_drawdown(returns),
    }
    if average_turnover is not None:
        summary["average_daily_turnover"] = float(average_turnover)
    return pd.Series(summary)
