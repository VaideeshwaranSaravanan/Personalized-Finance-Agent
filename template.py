import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "requirements.txt",
    "setup.py",
    "Home.py",
    "Results/",
    "Data/",
    "research/trials.ipynb"
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