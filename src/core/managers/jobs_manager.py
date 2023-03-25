import json
import os
import shutil

from common.env import DEFAULT_DIR_PATH, JOBS_FILE_PATH, LOGS_DIR_PATH
from core.models.job import Job
from database.json_database import JsonDatabase

JOBS_MODEL = "jobs"
json_db = JsonDatabase(DEFAULT_DIR_PATH)

class JobsManager:
  @staticmethod
  def InitPath() -> None:
    dirs = [DEFAULT_DIR_PATH, LOGS_DIR_PATH]
    for path in dirs:
      if not os.path.isdir(path):
        os.mkdir(path)

  @staticmethod
  def Create(name: str, command: str) -> None:
    JobsManager.Save(Job(name, command))

  @staticmethod
  def Run(name: str) -> None:
    job = JobsManager.Load(name)
    job.run()
    JobsManager.Save(job)

  @staticmethod
  def Kill(name: str) -> None:
    job = JobsManager.Load(name)
    job.kill()
    JobsManager.Save(job)

  @staticmethod
  def Save(job: Job) -> None:
    json_db.write_key(JOBS_MODEL, job.get_name(), {
      "command": job.get_command(),
      "pid": job.get_pid(),
    })

  @staticmethod
  def Load(name: str) -> Job:
    item = json_db.read_key(JOBS_MODEL, name)
    if not item:
      raise Exception("Job not found")

    return Job(name, item.get("command"), item.get("pid"))

  @staticmethod
  def List() -> list[Job]:
    jobs = []
    for item in json_db.read(JOBS_MODEL).items():
      jobs.append(Job(item[0], item[1].get("command"), item[1].get("pid")))

    return jobs

  @staticmethod
  def Remove(name: str) -> None:
    json_db.delete_key(JOBS_MODEL, name)
    logs_path = f"{LOGS_DIR_PATH}/{name}"
    if os.path.isdir(logs_path):
      shutil.rmtree(logs_path)
