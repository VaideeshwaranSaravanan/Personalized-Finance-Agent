# finance_brain.py
from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool
from src.helper import Helper

# Import your subagents
from agents.Mortgage_agent import Mortgage_agent
from agents.Stock_agent import StockAgent  # renamed earlier
from agents.Stock_monitoring_agent import StockMonitoringAgent
from tools.Finance_Info_Agent import FinanceInfoAgent   # formerly InterestFinder
#from agents.Router_agent import RouterAgent


class FinanceBrain:
    def __init__(self):
        # Instantiate subagents
        #self.router = RouterAgent().agent
        self.mortgage = Mortgage_agent().agent
        self.stock = StockAgent().agent
        self.monitor = StockMonitoringAgent().agent
        self.fact = FinanceInfoAgent().agent_FinanceInfo

        self.parallel_aggregator = LlmAgent(
            name = "Aggregator_agent",
            model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=Helper.Http_options()
    ),
    # It uses placeholders to inject the outputs from the parallel agents, which are now in the session state.
    instruction="""Combine these two outputs into a single summary:

    **Output from Stock Agent:**
    {Stock_Output}
    
    **Output from Stock Monitoring Agent:**
    {Stock_Monitor_Output}
    
    Your summary should combine and and provide the correct valuable output""",
    output_key="Aggregator_Output",
    )

        self.parallel_stock = ParallelAgent(
            name = "ParallelStock",
            sub_agents=[self.stock, self.monitor]
        )
        self.combined = SequentialAgent(
            name = "ParallelStockTeam",
            sub_agents=[self.parallel_stock, self.parallel_aggregator]
        )
        # FinanceBrain LLM
        self.agent = LlmAgent(
            name="FinanceBrain",
            model=Gemini(model="gemini-2.5-flash-lite",
                         retry_options=Helper.Http_options()),

            # ⬇⬇⬇ CRITICAL INSTRUCTION SET (DO NOT CHANGE) ⬇⬇⬇
            instruction="""
            You are the FinanceBrain — the master coordinator for all financial workflows.

            ──────────────────────────────────────────────
            YOUR JOB
            ──────────────────────────────────────────────
            The RouterAgent gives you a category: {route_output}

            Based on that category, you MUST route the user query to one of the following:

            1. MortgageAgent
            2. StockAgent
            3. StockMonitoringAgent
            4. FactExtractionAgent (generic financial questions)
            5. ParallelAgent (Stock + StockMonitor)
            6. Ask user for clarification (ASK_CLARIFY)
            7. Reject with domain warning (OUT_OF_DOMAIN)

            You NEVER answer directly.  
            You only call subagents or ask a question.

            ──────────────────────────────────────────────
            ALLOWED CATEGORIES FROM ROUTER
            ──────────────────────────────────────────────
            - MORTGAGE
            - STOCK
            - STOCK_MONITOR
            - STOCK_STOCKMONITOR
            - GENERIC_FINANCE
            - ASK_CLARIFY
            - OUT_OF_DOMAIN

            ──────────────────────────────────────────────
            DIP/High LOGIC (IMPORTANT)
            ──────────────────────────────────────────────
            If user requests:
                “dips”, “drop”, “falls by %”, “monitor for drop”, "increase", "Shoots by %", "monitor for raises" etc.

            AND they did NOT give a percentage or threshold,
            you MUST send:
                "ASK_CLARIFY"

            If user says:
                “10 percent dip”, “drop below 250”, "increase by 10%" etc.
            → Forward EXACT data to StockMonitoringAgent.

            FinanceBrain NEVER:
            - Computes percentages
            - Computes thresholds
            - Retrieves prices
            - Starts scheduler
            - Adds alerts

            Those actions belong to subagents.

            ──────────────────────────────────────────────
            OUT OF DOMAIN RULE
            ──────────────────────────────────────────────
            If Router classifies as OUT_OF_DOMAIN:
            Reply:
            “This assistant is specialized only in financial queries.
            Please ask a finance-related question.”

            ──────────────────────────────────────────────
            WORKFLOW RULES
            ──────────────────────────────────────────────
            For:
            • STOCK → call StockAgent only ("Stock_agent" tool) 
            • MORTGAGE → call MortgageAgent only ("Mortgage_agent" tool) 
            • GENERIC_FINANCE → call FinanceInfoAgent only ("FinanceInfoAgent" tool) 
            • STOCK_MONITOR → call StockMonitoringAgent only ("monitoring_agent" tool) 
            • STOCK_STOCKMONITOR →
                Call combined ("ParallelStockTeam" tool) 
            ──────────────────────────────────────────────
            YOUR OUTPUT
            ──────────────────────────────────────────────
            You MUST:
            - Produce raw subagent output
            - NO formatting
            - NO friendliness
            - NO rewriting
            ToneAgent will do the final formatting.

            """,

            tools=[
                #AgentTool(self.router),
                AgentTool(self.mortgage),
                AgentTool(self.stock),
                AgentTool(self.monitor),
                AgentTool(self.fact),
                AgentTool(self.combined)
            ],
            output_key="FinBrain_output"
        )
