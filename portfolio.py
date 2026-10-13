import pandas as pd

def portfolio_returns(returns, weights):

    if len(weights) != returns.shape[1]:
        raise ValueError(
            f"Got {len(weights)} weights for {returns.shape[1]} tickers - these must match 1:1, in the same column order as 'returns'."
        ) 

    weight_sum = sum(weights)
    if abs(weight_sum - 1.0) > 1e-4:
        raise ValueError(
            f"Weights must sum to 1.0, got {weight_sum:.6f} instead."
        )

    weighted_returns = returns.mul(weights, axis='columns')
    portfolio_return = weighted_returns.sum(axis= 'columns')

    return portfolio_return

def portfolio_value(weighted_returns, initial_investment=10000):
    weighted_cumulative_returns = (1 + weighted_returns).cumprod()
    weighted_portfolio_return = weighted_cumulative_returns * initial_investment

    return weighted_portfolio_return

if __name__ == "__main__":
    from data import fetch_prices
    from metrics import daily_returns

    weights = [0.5, 0.3, 0.2]
    prices = fetch_prices(["AAPL", "EXPD"], "2021-01-01", "2024-01-01")
    returns = daily_returns(prices)
    
    result = portfolio_returns(returns, weights)
    print(result.head())
    print(result.tail())
