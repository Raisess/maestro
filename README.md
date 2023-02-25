# Maestro

This is a simple CLI to manage background jobs (processes).

## How to use?

**create**: Create a new job.

```shell
maestro create <name> "<command>"
```

- NOTE: This command do not execute the job command, you have to use `run` command.

**run**: Run a job.

```shell
maestro run <name>
```

- NOTE: You have to create a job before running.

**list**: List all created jobs.

```shell
maestro list
```

**logs**: Show logs of a specific job.

```shell
maestro logs <name>
```

- NOTE: This command don't have a hot reload.

**clear-logs**: Clear all logs for all jobs.

```shell
maestro clear-logs
```
