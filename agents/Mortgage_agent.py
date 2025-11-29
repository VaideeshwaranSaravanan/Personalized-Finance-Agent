#Mortgage Agent
from src.helper import Helper
from tools.calculator_agent_tool import calculator_agent
from tools.Finance_Info_Agent import FinanceInfoAgent
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool

class Mortgage_agent:
    def __init__(self):
            self.interest_finder = FinanceInfoAgent().agent_interest
            self.Calculator = calculator_agent().agent

            self.agent = LlmAgent(
            name="Mortgage_agent",
            model=Gemini(model="gemini-2.5-flash-lite", retry_options=Helper.Http_options()),
            # Updated instruction
            instruction="""
        You are the Mortgage Orchestration Agent.

        Input = User Query

        Your responsibilities:

        1. If the user asks for a mortgage interest rate:
        - Call Interest_finder tool.
        - Return ONLY the numeric rate.

        2. If the user asks for a mortgage calculation:
        - Call Calculator_agent tool with the keyword "Mortgage calculator".
        - Pass all user parameters given.
        - Forward EXACTLY the Python execution output to the user.

        3. NEVER generate calculations or code yourself.
        4. ALWAYS return tool outputs directly without modification.
        5. If information is missing (e.g., bank interest rate),
        FIRST call the Interest_finder agent to obtain the numeric rate,
        THEN call the calculation agent.

        You are the coordinator - you decide which agent runs first."""
        ,
            tools=[
                AgentTool(self.interest_finder), AgentTool(self.Calculator)  
            ],

            output_key="Mortgage_output"
        )
            

'''
agent = LlmAgent(
    name="enhanced_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=Helper.Http_options()),
    # Updated instruction
    instruction="""
You are now a calculator assistant.

RULES:
1. If the task is to find answer for ANY calculation - simple or complex - you MUST call the calculator_agent tool and create the required Python function to calculate and execute it.
2. You MUST pass the user's entire request directly to the tool.
3. You MUST NOT generate any Python code yourself.
4. After the tool runs and executes the code, you MUST return the tool's result to the user.
"""
,
    tools=[
        AgentTool(agent=calculator_agent().agent),  # Using another agent as a tool!
    ],
)

#This code is just for now

Sample runs - 
runner = InMemoryRunner(agent=agent)
response = await runner.run_debug(
    "What is the monthly mortgage payment that I have to pay for a $620,000 home, $120,000 downpayment, 5 percent interest, 25 years."
)

 ### Created new session: debug_session_id

User > What is the monthly mortgage payment that I have to pay for a $620,000 home, $120,000 downpayment, 5 percent interest, 25 years.
enhanced_agent > The monthly mortgage payment for the house would be approximately $3,597.58.

response1 = await runner.run_debug(
    "I want a full amortization schedule for a $700,000 mortgage, $100,000 downpayment, 4.2% interest, 30 years. "
)

User > I want a full amortization schedule for a $700,000 mortgage, $100,000 downpayment, 4.2% interest, 30 years. 
enhanced_agent > Here is the amortization schedule for your mortgage:

Month | Payment   | Interest Paid | Principal Paid | Remaining Balance
----------------------------------------------------------------------
1     | 2922.96   | 2100.00       | 822.96         | 599177.04
2     | 2922.96   | 2097.07       | 825.89         | 598351.15
3     | 2922.96   | 2094.12       | 828.84         | 597522.31
4     | 2922.96   | 2091.14       | 831.82         | 596690.49
5     | 2922.96   | 2088.14       | 834.82         | 595855.67
6     | 2922.96   | 2085.12       | 837.84         | 595017.83
7     | 2922.96   | 2082.08       | 840.88         | 594176.95
8     | 2922.96   | 2079.02       | 843.94         | 593333.01
9     | 2922.96   | 2075.95       | 847.01         | 592486.00
10    | 2922.96   | 2072.85       | 850.11         | 591635.89
11    | 2922.96   | 2069.73       | 853.23         | 590782.66
12    | 2922.96   | 2066.60       | 856.36         | 589926.30
13    | 2922.96   | 2063.44       | 859.52         | 589066.78
14    | 2922.96   | 2060.27       | 862.69         | 588204.09
15    | 2922.96   | 2057.07       | 865.89         | 587338.20
16    | 2922.96   | 2053.85       | 869.11         | 586469.09
17    | 2922.96   | 2050.62       | 872.34         | 585596.75
...
357   | 2922.96   | 340.54        | 2582.42        | 140240.00
358   | 2922.96   | 340.23        | 2582.73        | 140240.00
359   | 2922.96   | 339.91        | 2583.05        | 140240.00
360   | 2922.96   | 339.60        | 2583.36        | 140240.00


agent = LlmAgent(
    name="enhanced_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=Helper.Http_options()),
    # Updated instruction
    instruction="""
You are now an Interest Search assistant.

RULES:
Your responsibilities:

1. If the user asks for a mortgage interest rate:
   - Call InterestSearchAgent tool.
   - Return the numeric rate and Bank name.
2. If the location/country is not given, try looking up and extract the Country name from the given name.
3. If cannot find the country or any countries other than Canada or US is identified, prompt for the country name strictly giving two options: Canada or US.

"""
,
    tools=[
        AgentTool(agent=Interest_Finder_Agent().agent),  # Using another agent as a tool!
    ],
)
'''