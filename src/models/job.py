import os
import signal
import subprocess
import time
from dataclasses import dataclass

from env import LOGS_DIR_PATH

@dataclass
class JobStatus:
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

    if self.status() != JobStatus.RUNNING:
      raise Exception("Process failed to start")

  def kill(self) -> None:
    if self.status() == JobStatus.STOPPED:
      raise Exception("Process not running, or it can be using another PID")

    os.kill(self.__pid, signal.SIGKILL)

  def status(self) -> JobStatus:
    if self.__pid == 0:
      return JobStatus.STOPPED

    try:
      cmdline_f = open(f"/proc/{self.__pid}/cmdline")
      job_cmd = "".join(self.__command.split(" "))
      pid_cmd = "".join(cmdline_f.read().strip().split("\x00"))
      cmdline_f.close()
      if job_cmd == pid_cmd:
        return JobStatus.RUNNING

      return JobStatus.STOPPED
    except:
      return JobStatus.STOPPED

  def __get_logfile_path(self) -> str:
    path = f"{LOGS_DIR_PATH}/{self.__name}"
    if not os.path.isdir(path):
      os.mkdir(path)

    return f"{path}/{self.__timestamp()}"

  def __timestamp(self) -> int:
    return int(time.time_ns() / 100000)
