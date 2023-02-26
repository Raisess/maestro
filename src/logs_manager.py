import os
import shutil

from env import LOGS_DIR_PATH
from job.log import Log

class LogsManager:
  @staticmethod
  def List(job_name: str) -> list[Log]:
    all_logs = []
    if os.path.isdir(LOGS_DIR_PATH):
      dir_path = LogsManager.__GetPath(job_name)
      files = os.listdir(dir_path)
      files.sort()
      files.reverse()
      for filename in files:
        with open(f"{dir_path}/{filename}", "r") as log_file:
          data = log_file.read().split("\n")
          data.reverse()
          all_logs.append(Log(filename, "\n".join(data)))

    return all_logs

  @staticmethod
  def Clear(job_name: str) -> None:
    dir_path = LogsManager.__GetPath(job_name)
    shutil.rmtree(dir_path)

  @staticmethod
  def ClearAll() -> None:
    dirs = os.listdir(LOGS_DIR_PATH)
    for dir in dirs:
      shutil.rmtree(f"{LOGS_DIR_PATH}/{dir}")

  @staticmethod
  def __GetPath(job_name: str) -> str:
    dir_path = f"{LOGS_DIR_PATH}/{job_name}"
    if not os.path.isdir(dir_path):
      raise Exception("No logs for this job")

    return dir_path
