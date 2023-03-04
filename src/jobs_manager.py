import json
import os
import shutil

from env import DEFAULT_DIR_PATH, JOBS_FILE_PATH, LOGS_DIR_PATH
from models.job import Job

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
    data = JobsManager.__GetJobsFromFile()
    data[job.get_name()] = {
      "command": job.get_command(),
      "pid": job.get_pid(),
    }
    JobsManager.__UpdateJobsInFile(data)

  @staticmethod
  def Load(name: str) -> Job:
    job_data = JobsManager.__GetJobsFromFile().get(name)
    if not job_data:
      raise Exception("Job not found")

    return Job(name, job_data.get("command"), job_data.get("pid"))

  @staticmethod
  def List() -> list[tuple[str, str]]:
    return JobsManager.__GetJobsFromFile().items()

  @staticmethod
  def Remove(name: str) -> None:
    data = JobsManager.__GetJobsFromFile()
    data.pop(name)
    JobsManager.__UpdateJobsInFile(data)

    logs_path = f"{LOGS_DIR_PATH}/{name}"
    if os.path.isdir(logs_path):
      shutil.rmtree(logs_path)

  @staticmethod
  def __GetJobsFromFile() -> dict[str, str]:
    content = "{}"
    with open(JOBS_FILE_PATH, "r") as file:
      data = file.read()
      if data != "":
        content = data

    return json.loads(content)

  @staticmethod
  def __UpdateJobsInFile(data: dict[str, str]) -> None:
    with open(JOBS_FILE_PATH, "w") as file:
      file.write(json.dumps(data))
