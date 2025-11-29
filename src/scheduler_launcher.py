import subprocess
import psutil
import sys
import os
from typing import Dict, Any

SCHEDULER_MODULE = "src.scheduler"


def is_scheduler_running() -> bool:
    for proc in psutil.process_iter(["pid", "cmdline"]):
        try:
            cmd = " ".join(proc.info["cmdline"])
            if "src.scheduler" in cmd or "scheduler.py" in cmd:
                return True
        except:
            pass
    return False


def launch_scheduler() -> Dict[str, Any]:
    try:
        print("Launching scheduler in a NEW terminal...")

        subprocess.Popen(
            [
                "cmd.exe",
                "/k",                         # KEEP THE WINDOW OPEN
                sys.executable,
                "-m",
                SCHEDULER_MODULE
            ],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        return {"status": "success", "data": "Scheduler launched in new console."}

    except Exception as e:
        return {"status": "error", "error_message": str(e)}


if __name__ == "__main__":
    print(launch_scheduler())
