import pandas as pd
from dataclasses import dataclass

@dataclass
class BacktestResult:
    portfolio_cagr: float
    portfolio_volatility: float
    portfolio_sharpe_ratio: float
    portfolio_max_drawdown: float
    benchmark_cagr: float
    benchmark_volatility: float
    benchmark_sharpe_ratio: float
    benchmark_max_drawdown: float
    portfolio_values: pd.Series
    benchmark_values: pd.Series

from data import fetch_prices
from metrics import daily_returns, cagr, volatility, sharpe_ratio, max_drawdown
from portfolio import portfolio_returns
from portfolio import portfolio_value

def backtest(tickers, weights, start_date, end_date, benchmark_ticker="SPY"):

    benchmark = fetch_prices([benchmark_ticker], start_date, end_date)
    prices = fetch_prices(tickers, start_date, end_date)
    returns = daily_returns(prices)
    benchmark_returns = daily_returns(benchmark)
    weighted_portfolio_return = portfolio_returns(returns, weights)
    weighted_benchmark_return = portfolio_returns(benchmark_returns, [1.0])
    benchmark_values = portfolio_value(weighted_benchmark_return)
    portfolio_values = portfolio_value(weighted_portfolio_return)

    #Calling CAGR, volatility, sharpe ratio, and max drawdown functions for portfolio
    portfolio_cagr = cagr(portfolio_values)
    portfolio_volatility = volatility(weighted_portfolio_return)
    portfolio_sharpe_ratio = sharpe_ratio(portfolio_values, weighted_portfolio_return)
    portfolio_max_drawdown = max_drawdown(portfolio_values)

    #Calling CAGR, volatility, sharpe ratio, and max drawdown functions for benchmark
    benchmark_cagr = cagr(benchmark_values)
    benchmark_volatility = volatility(weighted_benchmark_return)
    benchmark_sharpe_ratio = sharpe_ratio(benchmark_values, weighted_benchmark_return)
    benchmark_max_drawdown = max_drawdown(benchmark_values)

    return BacktestResult(
        portfolio_cagr=portfolio_cagr,
        portfolio_volatility=portfolio_volatility,
        portfolio_sharpe_ratio=portfolio_sharpe_ratio,
        portfolio_max_drawdown=portfolio_max_drawdown,
        benchmark_cagr=benchmark_cagr,
        benchmark_volatility=benchmark_volatility,
        benchmark_sharpe_ratio=benchmark_sharpe_ratio,
        benchmark_max_drawdown=benchmark_max_drawdown,
        portfolio_values=portfolio_values,
        benchmark_values=benchmark_values
    )

if __name__ == "__main__":
    result = backtest(["AAPL", "EXPD", "PLTR"], [0.5, 0.3, 0.2], "2021-01-01", "2024-01-01")
    print(result)
