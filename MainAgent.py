# MainAgent.py

import os
import warnings
import asyncio

from config import GENAI_API_KEY

# -------------------------------------------------
# Environment setup
# -------------------------------------------------
os.environ["GOOGLE_API_KEY"] = GENAI_API_KEY
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
os.environ["ADK_SUPPRESS_NON_TEXT_WARNINGS"] = "1"

# -------------------------------------------------
# ADK imports
# -------------------------------------------------
from google.adk.agents import SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# -------------------------------------------------
# Your subagent imports
# -------------------------------------------------
from agents.Finance_brain import FinanceBrain
from agents.Router_agent import RouterAgent
from agents.Tone_agent import ToneAgent

# -------------------------------------------------
# Constants
# -------------------------------------------------
APP_NAME = "agents"
USER_ID = "default"
MODEL_NAME = "gemini-2.5-flash-lite"


# -------------------------------------------------
# Class: FinanceMainAgent
# -------------------------------------------------
class FinanceMainAgent:
    def __init__(self):

        # Instantiate individual subagents
        Route = RouterAgent().agent
        Brain = FinanceBrain().agent
        Tone = ToneAgent().agent

        # Main sequential agent
        self.agent = SequentialAgent(
            name="Finance_Agent",
            sub_agents=[Route, Brain, Tone]
        )

        # Session system
        self.session_service = InMemorySessionService()

        # Runner
        self.runner = Runner(
            agent=self.agent,
            app_name=APP_NAME,
            session_service=self.session_service
        )

    # -------------------------------------------------
    # run_session() — logic same as before
    # -------------------------------------------------
    async def run_session(
        self,
        user_queries: list[str] | str,
        session_name: str = "default"
    ):

        # Create or get session
        try:
            session = await self.session_service.create_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=session_name
            )
        except:
            session = await self.session_service.get_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=session_name
            )

        # Normalize input
        if isinstance(user_queries, str):
            user_queries = [user_queries]

        for query_text in user_queries:

            query = types.Content(
                role="user",
                parts=[types.Part(text=query_text)]
            )

            last_valid_output = None

            # Stream agent output
            async for event in self.runner.run_async(
                user_id=USER_ID,
                session_id=session.id,
                new_message=query
            ):
                if event.content and event.content.parts:
                    txt = event.content.parts[0].text
                    if txt and txt != "None":
                        last_valid_output = txt

            print(f"{MODEL_NAME} > {last_valid_output}")


# -------------------------------------------------
# Standalone main() for quick testing
# -------------------------------------------------
async def main():
    agent = FinanceMainAgent()

    print("Type 'exit' to quit.\n")

    while True:
        user_query = input("User_query: ")
        if user_query.lower().strip() == "exit":
            break

        await agent.run_session(
            user_queries=user_query,
            session_name="stateful-agentic-session"
        )


# -------------------------------------------------
# File entrypoint
# -------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
