#! /usr/bin/env python3

from yacli import CLI, Command

from cli.commands import *

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
