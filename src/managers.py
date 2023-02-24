import os
import shutil

from env import DEFAULT_DIR_PATH, JOBS_DIR_PATH, LOGS_DIR_PATH
from job.job import Job
from job.log import Log

class JobsManager:
  @staticmethod
  def InitPath() -> None:
    dirs = [DEFAULT_DIR_PATH, JOBS_DIR_PATH, LOGS_DIR_PATH]
    for dir in dirs:
      if not os.path.isdir(dir):
        os.mkdir(dir)

  @staticmethod
  def Create(name: str, command: str) -> Job:
    job_logs_dir_path = f"{LOGS_DIR_PATH}/{name}"
    if not os.path.isdir(job_logs_dir_path):
      os.mkdir(job_logs_dir_path)

    return Job(name, command)

  @staticmethod
  def Save(job: Job) -> None:
    file_path = f"{JOBS_DIR_PATH}/{job.get_name()}"
    with open(file_path, "w") as file:
      file.write(job.get_command())

  @staticmethod
  def Load(name: str) -> Job:
    file_path = f"{JOBS_DIR_PATH}/{name}"
    if not os.path.exists(file_path):
      raise Exception("This job don't exists")

    file = open(file_path, "r")
    job = Job(name, file.read())
    file.close()
    return job

  @staticmethod
  def ListNames() -> list[str]:
    if not os.path.isdir(JOBS_DIR_PATH):
      raise Exception("No jobs found")

    return os.listdir(JOBS_DIR_PATH)


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
