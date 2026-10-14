import pandas as pd
from dataclasses import dataclass

@dataclass
class BacktestResult:
    portfolio_cagr: float
    portfolio_volatility: float
    portfolio_sharpe_ratio: float
    portfolio_max_drawdown: float
    benchmark_ticker: str
    benchmark_cagr: float
    benchmark_volatility: float
    benchmark_sharpe_ratio: float
    benchmark_max_drawdown: float
    portfolio_values: pd.Series
    benchmark_values: pd.Series

