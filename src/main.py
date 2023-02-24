#! /usr/bin/env python3

from yacli import CLI, Command

from managers import JobsManager, LogsManager

class CreateJob(Command):
  def __init__(self):
    super().__init__(
      "create",
      "Create a new background job.\n\t\tE.g.: maestro <name> \"<command>\"",
      args_len=2
    )

  def handle(self, args: list[str]) -> None:
    JobsManager.InitPath()
    job = JobsManager.Create(name=args[0], command=args[1])
    JobsManager.Save(job)
    print(">>> Job created successfully!")


class RunJob(Command):
  def __init__(self):
    super().__init__(
      "run",
      "",
      args_len=1
    )

  def handle(self, args: list[str]) -> None:
    job = JobsManager.Load(name=args[0])
    job.run()
    print(">>> Job started successfully!")


class ListJobs(Command):
  def __init__(self):
    super().__init__("list", "")

  def handle(self, _: list[str]) -> None:
    print(">>> Available jobs:")
    for job_name in JobsManager.ListNames():
      print(f">>>>>> {job_name}")



class CheckLogs(Command):
  def __init__(self):
    super().__init__(
      "logs",
      "Get logs from a job and print it using `less`.\n\t\tE.g.: maestro <name>",
      args_len=1
    )

  def handle(self, args: list[str]) -> None:
    import os

    logs = []
    for log in LogsManager.List(job_name=args[0]):
      logs.extend([f"{log.filename()} | {entry}" for entry in log.data()])

    logs_txt = "\n".join(logs)
    os.system(f"echo \"{logs_txt}\" | less")


class ClearLogs(Command):
  def __init__(self):
    super().__init__("clear-logs", "Clear all logs.")

  def handle(self, _: list[str]) -> None:
    LogsManager.ClearAll()
    print(">>> Logs cleaned!")


if __name__ == "__main__":
  cli = CLI("maestro", [CreateJob(), RunJob(), ListJobs(), CheckLogs(), ClearLogs()])
  cli.handle()
