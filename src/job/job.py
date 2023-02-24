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
    os.system(f"{self.__command} > {self.__get_logfile()} 2>&1 &")

  def __get_logfile(self) -> str:
    return f"{LOGS_DIR_PATH}/{self.__name}/{self.__timestamp()}"

  def __timestamp(self) -> int:
    return int(time.time_ns() / 100000)
