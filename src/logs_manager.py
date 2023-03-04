import os

from env import LOGS_DIR_PATH
from models.log import Log

class LogsManager:
  @staticmethod
  def List(job_name: str) -> list[Log]:
    all_logs = []
    if os.path.isdir(LOGS_DIR_PATH):
      dir_path = LogsManager.__GetPath(job_name)
      files = LogsManager.__GetSortedFiles(dir_path)
      for filename in files:
        with open(f"{dir_path}/{filename}", "r") as log_file:
          all_logs.append(Log(filename, log_file.read()))

    return all_logs

  @staticmethod
  def Clear(job_name: str) -> None:
    dir_path = LogsManager.__GetPath(job_name)
    LogsManager.__ClearFiles(dir_path)

  @staticmethod
  def ClearAll() -> None:
    for dir in os.listdir(LOGS_DIR_PATH):
      LogsManager.__ClearFiles(f"{LOGS_DIR_PATH}/{dir}")

  @staticmethod
  def __ClearFiles(dir_path: str) -> None:
    files = LogsManager.__GetSortedFiles(dir_path)
    for idx, file in enumerate(files):
      path = f"{dir_path}/{file}"
      if idx == 0:
        LogsManager.__ClearFile(path)
        continue

      os.remove(path)

  @staticmethod
  def __ClearFile(path: str) -> None:
    with open(path, "w") as f:
      f.write("")

  @staticmethod
  def __GetSortedFiles(dir_path: str) -> list[str]:
    files = os.listdir(dir_path)
    files.sort()
    files.reverse()
    return files

  @staticmethod
  def __GetPath(job_name: str) -> str:
    dir_path = f"{LOGS_DIR_PATH}/{job_name}"
    if not os.path.isdir(dir_path):
      raise Exception("No logs for this job")

    return dir_path
