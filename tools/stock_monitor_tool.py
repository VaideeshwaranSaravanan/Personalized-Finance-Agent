import json
import os
from typing import Dict, Any
from datetime import datetime
import yfinance as yf

from tools.Yahoo_Finance_Function_tool import get_stock_yahoo
from src.scheduler_launcher import is_scheduler_running, launch_scheduler


class StockMonitorTool:
    """
    Unified tool class for:
    - Adding stock alerts
    - Checking alerts
    - Ensuring background scheduler is running
    """

    WATCHLIST_FILE = "stock_watchlist.json"

    # ─────────────────────────────────────────────
    # Internal Helpers
    # ─────────────────────────────────────────────
    def load_watchlist(self):
        """
        Load the JSON watchlist file.
        Returns dict with structure:
        {
            "watchlist": [
                {"symbol": "AAPL", "threshold": 150, "direction": "below", "last_notified": None}
            ]
        }
        """
        if not os.path.exists(self.WATCHLIST_FILE):
            return {"watchlist": []}
        try:
            with open(self.WATCHLIST_FILE, "r") as f:
                return json.load(f)
        except:
            return {"watchlist": []}

    def save_watchlist(self, data):
        """Save the updated watchlist to file."""
        with open(self.WATCHLIST_FILE, "w") as f:
            json.dump(data, f, indent=4)

    # ─────────────────────────────────────────────
    # ADK Tool: Ensure Scheduler Running
    # ─────────────────────────────────────────────
    def ensure_scheduler_running(self) -> Dict[str, Any]:
        """
        Ensures the stock monitoring scheduler is active.

        VALID:
            ensure_scheduler_running()

        INVALID:
            ensure_scheduler_running("start")
            ensure_scheduler_running(args={})

        Returns:
            dict: {"status": "success", "data": "..."} or {"status": "error", "error_message": "..."}
        """
        if is_scheduler_running():
            return {
                "status": "success",
                "data": "Scheduler already running."
            }

        return launch_scheduler()

    # ─────────────────────────────────────────────
    # ADK Tool: Add Stock Alert
    # ─────────────────────────────────────────────
    def add_stock_alert(self, symbol: str, threshold: float, direction: str) -> Dict[str, Any]:
        """
        Adds a stock alert and auto-starts the scheduler.

        VALID USAGE:
            add_stock_alert(symbol="AAPL", threshold=150, direction="below")
            add_stock_alert(symbol="TSLA", threshold=300, direction="above")

        INVALID USAGE:
            add_stock_alert(ticker="AAPL", price=150, dir="below")
            add_stock_alert({"symbol": "AAPL", "threshold": 150, "direction": "below"})

        Args:
            symbol (str): Stock ticker like "AAPL"
            threshold (float): Price threshold
            direction (str): "above" or "below"

        Returns:
            dict: success / error structure
        """
        try:
           # self.ensure_scheduler_running()

            data = self.load_watchlist()
            data["watchlist"].append({
                "symbol": symbol.upper(),
                "threshold": float(threshold),
                "direction": direction.lower(),
                "last_notified": None
            })

            self.save_watchlist(data)

            return {
                "status": "success",
                "data": f"Alert added: Notify when {symbol.upper()} goes {direction} {threshold}"
            }

        except Exception as e:
            return {"status": "error", "error_message": str(e)}

    # ─────────────────────────────────────────────
    # ADK Tool: Check Alerts
    # ─────────────────────────────────────────────

    def check_alerts1(self) -> Dict[str, Any]:
        """
        Evaluates stock alerts and returns triggered notifications.
        """
        try:
            data = self.load_watchlist()   # FIXED
            notifications = []

            for item in data["watchlist"]:
                symbol = item["symbol"]

                try:
                    yahoo_info = get_stock_yahoo(symbol)
                    price = yahoo_info["data"]["current_price"]
                except:
                    ticker = yf.Ticker(symbol)
                    price = ticker.info.get("regularMarketPrice")

                if price is None:
                    continue

                condition_met = (
                    (item["direction"] == "above" and price >= item["threshold"]) or
                    (item["direction"] == "below" and price <= item["threshold"])
                )

                if condition_met:
                    notifications.append({
                        "symbol": symbol,
                        "price": price,
                        "threshold": item["threshold"],
                        "message": f"{symbol} is now {price}, which is {item['direction']} {item['threshold']}"
                    })

                    item["last_notified"] = str(datetime.now())

            self.save_watchlist(data)

            return {"status": "success", "data": notifications}

        except Exception as e:
            return {"status": "error", "error_message": str(e)}


    def check_alerts(self) -> Dict[str, Any]:
        """
        Evaluates stock alerts and returns triggered notifications.

        VALID:
            check_alerts()

        INVALID:
            check_alerts(args={})
            check_alerts("now")

        Returns:
            dict with:
            {
                "status": "success",
                "data": [
                    {
                        "symbol": "AAPL",
                        "price": 149.2,
                        "threshold": 150,
                        "message": "AAPL is now 149.2, which is below 150"
                    }
                ]
            }
        """
        try:
            data = self.load_watchlist()
            notifications = []

            for item in data["watchlist"]:
                symbol = item["symbol"]

                try:
                    yahoo_info = get_stock_yahoo(symbol)
                    price = yahoo_info["data"]["current_price"]
                except:
                    ticker = yf.Ticker(symbol)
                    price = ticker.info.get("regularMarketPrice")

                if price is None:
                    continue

                condition_met = (
                    (item["direction"] == "above" and price >= item["threshold"]) or
                    (item["direction"] == "below" and price <= item["threshold"])
                )

                if condition_met:
                    notifications.append({
                        "symbol": symbol,
                        "price": price,
                        "threshold": item["threshold"],
                        "message": f"{symbol} is now {price}, which is {item['direction']} {item['threshold']}"
                    })

                    item["last_notified"] = str(datetime.now())

            self.save_watchlist(data)

            return {"status": "success", "data": notifications}

        except Exception as e:
            return {"status": "error", "error_message": str(e)}
