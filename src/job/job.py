import os
import time

from env import LOGS_DIR_PATH

class Job:
  def __init__(self, name: str, command: str):
    self.__name = name.strip()
    self.__command = command.strip()

  def get_name(self) -> str:
    return self.__name

  def get_command(self) -> str:
    return self.__command

  def run(self) -> None:
    self.__create_logs_dir()
    logfile = f"{self.__get_logs_path()}/{self.__timestamp()}"
    os.system(f"{self.__command} > {logfile} 2>&1 &")

  def __create_logs_dir(self) -> None:
    if not os.path.isdir(self.__get_logs_path()):
      os.mkdir(self.__get_logs_path())

  def __get_logs_path(self) -> str:
    return f"{LOGS_DIR_PATH}/{self.__name}"

  def __timestamp(self) -> int:
    return int(time.time_ns() / 100000)
