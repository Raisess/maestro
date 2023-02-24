import os

USER = os.getenv("USER")
DEFAULT_DIR_PATH = os.getenv("MAESTRO_PATH") or f"/home/{USER}/.maestro"
JOBS_DIR_PATH = f"{DEFAULT_DIR_PATH}/jobs"
LOGS_DIR_PATH = f"{DEFAULT_DIR_PATH}/logs"
