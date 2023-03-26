import os

USER = os.getenv("USER")
DEFAULT_DIR_PATH = os.getenv("MAESTRO_PATH") or f"/home/{USER}/.maestro"
LOGS_DIR_PATH = f"{DEFAULT_DIR_PATH}/logs"
JOBS_FILE_PATH = f"{DEFAULT_DIR_PATH}/jobs.json"

WEB_SESSION_DURATION_MINUTES = int(os.getenv("WEB_SESSION_DURATION_MINUTES") or 60)
