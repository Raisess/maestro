import os
import signal
import subprocess
import time
from dataclasses import dataclass
from uuid import uuid4

from env import LOGS_DIR_PATH

@dataclass
class JobState:
  STOPPED = 0
  RUNNING = 1


class Job:
  def __init__(self, name: str, command: str, pid: int = 0):
    self.__name = name
    self.__command = command.strip()
    self.__pid = pid

  def get_name(self) -> str:
    return self.__name

  def get_command(self) -> str:
    return self.__command

  def get_pid(self) -> int:
    return self.__pid

  def run(self) -> None:
    stdout = subprocess.getoutput(f"{self.__command} > {self.__get_logfile_path()} 2>&1 | echo $$ &")
    self.__pid = int(stdout) + 1
    time.sleep(1)

  def kill(self) -> None:
    if self.state() == JobState.STOPPED:
      raise Exception("Process not running, or it can be using another PID")

    os.kill(self.__pid, signal.SIGTERM)
    time.sleep(1)

  def state(self) -> JobState:
    if self.__pid == 0:
      return JobState.STOPPED

    try:
      cmdline_f = open(f"/proc/{self.__pid}/cmdline")
      pid_cmd = cmdline_f.read().replace("\000", " ").strip()
      cmdline_f.close()
      if pid_cmd.__contains__(self.__command) or self.__command.__contains__(pid_cmd):
        return JobState.RUNNING

      return JobState.STOPPED
    except:
      return JobState.STOPPED

  def __get_logfile_path(self) -> str:
    path = f"{LOGS_DIR_PATH}/{self.__name}"
    if not os.path.isdir(path):
      os.mkdir(path)

    return f"{path}/{str(uuid4())}"
