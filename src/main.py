#! /usr/bin/env python3

from yacli import CLI, Command

from core.managers.jobs_manager import JobsManager
from core.managers.logs_manager import LogsManager

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
    super().__init__("run", "Start a job.\n\t\tE.g.: maestro run <name>", args_len=1)

  def handle(self, args: list[str]) -> None:
    job = JobsManager.Load(name=args[0])
    job.run()
    JobsManager.Save(job)
    print(">>> Job started successfully!")


class KillJob(Command):
  def __init__(self):
    super().__init__("kill", "Kill a job.\n\t\tE.g.: maestro kill <name>", args_len=1)

  def handle(self, args: list[str]) -> None:
    job = JobsManager.Load(name=args[0])
    job.kill()
    print(">>> Job killed successfully!")


class RemoveJob(Command):
  def __init__(self):
    super().__init__("remove", "Remove a job.\n\t\tE.g.: maestro remove <name>", args_len=1)

  def handle(self, args: list[str]) -> None:
    JobsManager.Remove(name=args[0])
    print(">>> Job removed successfully!")


class ListJobs(Command):
  def __init__(self):
    super().__init__("list", "List logs from a specific job.")

  def handle(self, _: list[str]) -> None:
    print(">>> Available jobs:")
    for job in JobsManager.List():
      cpu_usage = "%.2f" % job.cpu_usage()
      state = "Running" if job.state() == 1 else "Stopped"
      print(f">>>>>> {job.get_name()}: {job.get_command()} | CPU: {cpu_usage} | State: {state}")


class CheckLogs(Command):
  def __init__(self):
    super().__init__(
      "logs",
      "Get logs from a job and print it using `less`.\n\t\tE.g.: maestro logs <name>",
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
    super().__init__("clear-logs", "Clear logs.")

  def handle(self, args: list[str]) -> None:
    if len(args) > 0:
      LogsManager.Clear(job_name=args[0])
    else:
      prompt = input("Are you sure you want to clear all logs? [Y/n] ")
      if prompt.lower() == "y":
        LogsManager.ClearAll()
        print(">>> Logs cleaned!")


class Serve(Command):
  def __init__(self):
    super().__init__(
      "serve",
      "Create a local server providing a web interface at http://localhost:<port>.\n\t\t"
      "E.g.: maestro serve [port]"
    )

  def handle(self, args: list[str]) -> None:
    from web.server import app
    port = int(args[0]) if len(args) > 0 else 6969
    host = args[1] if len(args) > 1 else "127.0.0.1"
    app.run(host, port)


if __name__ == "__main__":
  cli = CLI("maestro", [
    CreateJob(),
    RunJob(),
    KillJob(),
    RemoveJob(),
    ListJobs(),
    CheckLogs(),
    ClearLogs(),
    Serve()
  ])
  cli.handle()
