import yfinance as yf
from typing import Dict, Any
import pandas as pd

def get_stock_yahoo(symbol: str, period: str="1mo") -> Dict[str, Any]:
    
    """
    Fetch real-time and historical stock data from Yahoo Finance.
    Cleans NaN values and converts datetimes to JSON-safe strings.

    Args:
        symbol (str): Ticker symbol, e.g., "AAPL", "MSFT", "GOOG".
        period (str): Stock period of the Ticker, e.g., 1 day, 5 days, 1 month. By default, the value is "1mo"

    Returns:
        dict: {
            "status": "success",
            "data": {
                "symbol": str,
                "current_price": float,
                "history": list[dict],   # last 30 days OHLC
            }
        }
        OR, on failure:
        {
            "status": "error",
            "error_message": str
        }

    Notes:
        - Uses yfinance (unofficial Yahoo Finance API)
        - Provides last 1 month of daily historical data
        - Use inside ADK by adding to tools=[get_stock_yahoo]
    """
    try:
        ticker = yf.Ticker(symbol)

        current_price = ticker.info.get("regularMarketPrice")
        if current_price is None:
            return {
                "status": "error",
                "error_message": f"Unable to fetch price for {symbol}"
            }

        # Fetch history
        history_df = ticker.history(period=period)

        # Replace NaN with None
        history_df = history_df.replace({pd.NA: None, float("nan"): None})

        # Convert datetime index to string
        history_df.reset_index(inplace=True)
        history_df["Date"] = history_df["Date"].astype(str)

        # Convert to list of dictionaries
        history_list = history_df.to_dict(orient="records")

        return {
            "status": "success",
            "data": {
                "symbol": symbol,
                "current_price": current_price,
                "history": history_list
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }