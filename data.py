import pandas as pd
import yfinance as yf


def fetch_prices(tickers: list[str], start_date: str, end_date: str) -> pd.DataFrame:
    
    if not tickers:
        raise ValueError("tickers list cannot be empty.")

    raw = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )

    if raw.empty:
        raise ValueError(
            f"No price data returned for tickers={tickers}, "
            f"start={start_date}, end={end_date}."
        )

    if isinstance(raw.columns, pd.MultiIndex):
        prices = raw["Close"]
    else:
        prices = raw[["Close"]]
        prices.columns = tickers

    missing = prices.columns[prices.isna().all()].tolist()
    if missing:
        raise ValueError(f"No data found for ticker(s): {missing}")

    prices = prices.dropna(how="any")

    return prices

def fetch_risk_free_rate(start_date, end_date) -> float:
    treasury_data = fetch_prices(["^TNX"], start_date, end_date)
    risk_free_rate = treasury_data["^TNX"].mean() / 100

    return risk_free_rate
