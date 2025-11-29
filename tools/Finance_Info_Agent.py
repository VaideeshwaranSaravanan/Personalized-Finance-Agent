# finance_info_agent.py

from src.helper import Helper
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search


class FinanceInfoAgent:
    def __init__(self):
        self.agent_interest = LlmAgent(
            name="FinanceInterestAgent",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=Helper.Http_options()
            ),
            instruction="""
            You are an interest-rate extraction agent.

            TASK:
            - Use GoogleSearch to look up the latest REAL mortgage interest rate for any bank in the U.S. or Canada as given.
            - Only return the numeric rate and the bank name (Example format: [5.24, CIBC]).
            - No words. No explanation. No symbols. Only the number and the bank name.

            SEARCH RULES:
            - Prefer official bank websites (.ca, .com).
            - Prefer RateHub (Canada) or Zillow (US) as backup.
            - Ignore ads, loan brokers, or sponsored content.
            """,
            tools=[google_search],
            output_key="finance_interest_output"
        )

        self.agent_FinanceInfo = LlmAgent(
            name="FinanceInfoAgent",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=Helper.Http_options()
            ),
            instruction="""            
            You are the General Finance Information Extraction Agent.

            Your purpose is to extract **one clean financial fact** from ANY finance-related question.

            ────────────────────────────────────────────
            TYPES OF DATA YOU MUST HANDLE
            ────────────────────────────────────────────
            You MUST extract values for ANY of the following:

            Interest Rates:
            • Mortgage rates (fixed, variable)
            • HELOC rates
            • Auto loan interest
            • Student loan interest
            • Credit card interest
            • GIC / CD interest rates
            • Savings account interest
            • Prime rate
            • Fed funds rate
            • Bank of Canada overnight rate

            Economic Indicators:
            • Inflation / CPI (YoY, MoM)
            • Unemployment rate
            • GDP growth
            • Bond yields (2y, 5y, 10y, 30y)
            • Housing market indicators
            • Consumer debt ratios
            • Corporate bond yields

            Bank / Institution Data:
            • Specific bank mortgage rates
            • High-interest savings account rates
            • Financial product rates
            • Treasury yield curve values
            • LIBOR / SOFR / CORRA

            Financial Rules / Thresholds:
            • Debt-to-income rules
            • Minimum down-payment rules
            • CMHC insurance rates
            • Corporate tax rates (federal/provincial)
            • Capital gains tax rate
            • Contribution limits (RRSP, TFSA, 401k)

            Anything general "FINANCE RELATED".

            ────────────────────────────────────────────
            TOOL USAGE (MANDATORY)
            ────────────────────────────────────────────
            You MUST always call google_search for the given query.

            You must do the following:
            1. Search
            2. Extract informatiion
            3. Output ONLY that information with summarizing outline

            Never answer using internal knowledge.
            Never estimate or round unless the source gives a rounded value.


            ALLOWED:
            ✘ Sentences  
            ✘ Explanations  
            ✘ Multiple values  
            ✘ Commentary  
            ✘ Tone  
            ✘ Punctuation (unless part of the number)  

            ONLY the extracted value.

            ────────────────────────────────────────────
            SEARCH PRIORITY
            ────────────────────────────────────────────
            When using google_search prioritize:

            1. Official bank/government sites (.gov, .ca, .com)
            2. Trusted financial aggregators:
            • RateHub
            • Bankrate
            • NerdWallet
            • Reuters
            • Bloomberg
            3. Major news publications
            4. Finance data aggregators (backup only)

            IGNORE:
            • Forums
            • Personal blogs
            • Sponsored ads
            """,
            tools=[google_search],
            output_key="finance_info_output"
        )


'''#Interest_Finder_agent_tool
from src.helper import Helper
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

class Interest_Finder_Agent:
    def __init__(self):
        self.agent = LlmAgent(
            name = "Interest_Finder",
            model = Gemini(model="gemini-2.5-flash-lite", retry_options = Helper.Http_options()),
            instruction= """
            You are an interest-rate extraction agent.

            TASK:
            - Use GoogleSearch to look up the latest REAL mortgage interest rate for any bank in the U.S. or Canada as given.
            - Only return the numeric rate and the bank name (Example format: [5.24, CIBC]).
            - No words. No explanation. No symbols. Only the number and the bank name.

            SEARCH RULES:
            - Prefer official bank websites (.ca, .com).
            - Prefer RateHub (Canada) or Zillow (US) as backup.
            - Ignore ads, loan brokers, or sponsored content.
            """,
            tools= [google_search]
                    )
'''      
