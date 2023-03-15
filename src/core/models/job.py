import os
import signal
import subprocess
import time
from dataclasses import dataclass

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
    self.__ensure_running()
    os.kill(self.__pid, signal.SIGTERM)

    while self.state() == JobState.RUNNING:
      time.sleep(1)

    self.__pid = 0

  def cpu_usage(self) -> float:
    try:
      self.__ensure_running()
    except:
      return 0

    stat = self.__get_procfile("stat").split(" ")
    clock_tick = int(subprocess.getoutput("getconf CLK_TCK"))
    proc_utime = float(stat[13]) / clock_tick
    proc_stime = float(stat[14]) / clock_tick
    proc_start_time = float(stat[21]) / clock_tick

    with open("/proc/uptime", "r") as file:
      sys_uptime = float(file.readline().split(" ")[0])

    proc_elapsed_time = sys_uptime - proc_start_time
    proc_usage = ((proc_utime + proc_stime) * 100) / proc_elapsed_time
    return proc_usage

  def state(self) -> JobState:
    if self.__pid == 0:
      return JobState.STOPPED

    try:
      pid_cmd = self.__get_procfile("cmdline").replace("\000", " ")
      if pid_cmd.__contains__(self.__command) or self.__command.__contains__(pid_cmd):
        return JobState.RUNNING

      return JobState.STOPPED
    except:
      return JobState.STOPPED

  def __get_logfile_path(self) -> str:
    path = f"{LOGS_DIR_PATH}/{self.__name}"
    if not os.path.isdir(path):
      os.mkdir(path)

    timestamp = int(time.time_ns() / 100000)
    return f"{path}/{timestamp}"

  def __get_procfile(self, file: str) -> str:
    with open(f"/proc/{self.__pid}/{file}", "r") as file:
      content = file.read().strip()

    return content

  def __ensure_running(self) -> None:
    if self.state() == JobState.STOPPED:
      raise Exception("Process not running, or it can be using another PID")
