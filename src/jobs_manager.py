import json
import os

from env import DEFAULT_DIR_PATH, JOBS_FILE_PATH, LOGS_DIR_PATH
from job.job import Job

class JobsManager:
  @staticmethod
  def InitPath() -> None:
    dirs = [DEFAULT_DIR_PATH, LOGS_DIR_PATH]
    for path in dirs:
      if not os.path.isdir(path):
        os.mkdir(path)

    files = [JOBS_FILE_PATH]
    for path in files:
      if not os.path.isfile(path):
        file = open(path, "w")
        file.close()

  @staticmethod
  def Create(name: str, command: str) -> Job:
    return Job(name, command)

  @staticmethod
  def Save(job: Job) -> None:
    r_file = open(JOBS_FILE_PATH, "r")
    content = r_file.read()
    r_file.close()
    if content == "":
      content = "{}"

    w_file = open(JOBS_FILE_PATH, "w")
    data: dict = json.loads(content)
    data[job.get_name()] = job.get_command()
    w_file.write(json.dumps(data))

  @staticmethod
  def Load(name: str) -> Job:
    file = open(JOBS_FILE_PATH, "r")
    data: dict = json.load(file)
    job_command = data.get(name)
    if not job_command:
      raise Exception("Job not found")

    file.close()
    return Job(name, job_command)

  @staticmethod
  def List() -> list[tuple[str, str]]:
    file = open(JOBS_FILE_PATH, "r")
    data: dict = json.load(file)
    return data.items()
