import pandas as pd
from data import fetch_risk_free_rate

def daily_returns(prices: pd.DataFrame | pd.Series) -> pd.DataFrame | pd.Series:
    returns = prices.pct_change()
    returns = returns.dropna(how="all")

    return returns

def cagr(prices):
    first_timestamp = prices.index.min()
    last_timestamp = prices.index.max()
    first_price = prices.loc[first_timestamp]
    last_price = prices.loc[last_timestamp]
    years = (last_timestamp - first_timestamp).days / 365.25
    annual_returns = (last_price / first_price) ** (1 / years) - 1

    return annual_returns

def volatility(returns):
    std = returns.std()
    annual_std = std * (252 ** 0.5)

    return annual_std

def sharpe_ratio(prices, returns):
    ticker_returns = cagr(prices)
    ticker_std = volatility(returns)
    risk_free_rate = fetch_risk_free_rate(prices.index.min(), prices.index.max())
    ticker_sharpe_ratio = (ticker_returns - risk_free_rate) / ticker_std

    return ticker_sharpe_ratio

def max_drawdown(prices):
    running_max = prices.cummax()
    ticker_drawdown = (running_max - prices) / running_max
    ticker_max_drawdown = ticker_drawdown.max()

    return ticker_max_drawdown 

if __name__ == "__main__":
    from data import fetch_prices

    prices = fetch_prices(["AAPL"], "2021-01-01", "2024-01-01")
    print(prices.head())
    print(prices.tail())
    print(cagr(prices))
    returns = daily_returns(prices)
    print(volatility(returns))
    print(sharpe_ratio(prices, returns))
    print(max_drawdown(prices))