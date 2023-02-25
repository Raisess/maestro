import os
import shutil

from env import LOGS_DIR_PATH
from job.log import Log

class LogsManager:
  @staticmethod
  def List(job_name: str) -> list[Log]:
    all_logs = []
    if os.path.isdir(LOGS_DIR_PATH):
      dir_path = f"{LOGS_DIR_PATH}/{job_name}"
      if not os.path.isdir(dir_path):
        raise Exception("No logs for this job")

      files = os.listdir(dir_path)
      files.sort()
      files.reverse()
      for filename in files:
        with open(f"{dir_path}/{filename}", "r") as log_file:
          all_logs.append(Log(filename, log_file.read()))

    return all_logs

  @staticmethod
  def ClearAll() -> None:
    shutil.rmtree(LOGS_DIR_PATH)
