from tools.stock_monitor_tool import StockMonitorTool
from src.helper import Helper
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner

import os
from config import GENAI_API_KEY

os.environ["GOOGLE_API_KEY"] = GENAI_API_KEY
# ─────────────────────────────────────────────
# Instantiate the Stock Monitor
# ─────────────────────────────────────────────
monitor = StockMonitorTool()


# ─────────────────────────────────────────────
# Monitoring Agent (Scheduler auto-starts inside add_stock_alert)
# ─────────────────────────────────────────────
agent = LlmAgent(
    name="monitoring_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=Helper.Http_options()
    ),

    instruction="""
You are the Stock Monitoring Agent.

Your ONLY responsibilities:
1. Add stock alerts
2. Check existing alerts
3. Ensure the scheduler is running when explicitly requested

────────────────────────────────────────
TOOL USAGE RULES
────────────────────────────────────────

You MUST use these exact tool signatures:

1. add_stock_alert(symbol: str, threshold: float, direction: str)
2. check_alerts()
3. ensure_scheduler_running()

Never add extra arguments.
Never rename arguments.
Never wrap arguments inside dictionaries.
Never pass positional arguments that don't match.
Only call the tools using the exact parameter names above.

────────────────────────────────────────
WHEN TO CALL WHICH TOOL
────────────────────────────────────────

• User wants to create an alert:
    → Call add_stock_alert(
          symbol="AAPL",
          threshold=150,
          direction="below"
      )

• User asks to "check alerts" or "show notifications":
    → Call check_alerts()

• User asks "start scheduler" or "is scheduler running":
    → Call ensure_scheduler_running()

────────────────────────────────────────
RULES
────────────────────────────────────────
- Do NOT analyze or interpret stock prices.
- Do NOT perform financial predictions.
- Do NOT use Google Search or Yahoo Finance directly.
- ONLY manage stock alerts and monitoring.

Keep responses short and strictly operational.
"""
,

    # Tools exposed to the agent
    tools=[
        monitor.add_stock_alert,          # Auto-starts scheduler internally
        monitor.check_alerts,             # Scheduler will call this too
        monitor.ensure_scheduler_running  # Exposed only for explicit user requests
    ]
)

import asyncio

async def main():
    runner = InMemoryRunner(agent=agent)
    response = await runner.run_debug("start monitoring tesla for dips.")
    #print(response)

asyncio.run(main())
