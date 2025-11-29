import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    "MainAgent.py",
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    "src/scheduler.py",
    "src/scheduler_launcher.py",
    "tools/calculator_agent_tool.py",
    "tools/Finance_info_Agent.py",
    "tools/Yahoo_Finance_Function_tool.py",
    "tools/stock_monitor_tool.py",
    "tools/calculator_agent_tool.py",
    "tools/__init__.py",
    "agents/Tone_agent.py",
    "agents/Router_agent.py",
    "agents/Finance_brain.py",
    "agents/Mortgage_agent.py",
    "agents/Stock_agent.py",
    "agents/Stock_monitoring_agent.py",
    "agents/__init__.py",
    ".env",
    "requirements.txt",
    "setup.py",
    "app.py",
    "Results/",
    "Data/",
    "config.py",
    "research/trials.ipynb",
    "research/trials.py"
]

for filepath1 in list_of_files: 
    filepath = Path(filepath1) 

    if str(filepath1).endswith("/"): 
        os.makedirs(filepath, exist_ok=True) 
        logging.info(f"Creating empty directory: {filepath1}") 
        continue

    filedir, filename = os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filename} already exits!")