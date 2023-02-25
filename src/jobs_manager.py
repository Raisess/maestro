import os

from env import DEFAULT_DIR_PATH, JOBS_DIR_PATH, LOGS_DIR_PATH
from job.job import Job

class JobsManager:
  @staticmethod
  def InitPath() -> None:
    dirs = [DEFAULT_DIR_PATH, JOBS_DIR_PATH, LOGS_DIR_PATH]
    for dir in dirs:
      if not os.path.isdir(dir):
        os.mkdir(dir)

  @staticmethod
  def Create(name: str, command: str) -> Job:
    job = Job(name, command)
    if not os.path.isdir(job.get_logs_path()):
      os.mkdir(job.get_logs_path())

    return job

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
