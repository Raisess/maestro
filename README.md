# Maestro

This is a simple cli and web app to manage background jobs (processes). [Only for Linux]

## How to use?

**init**: Init maestro, create the required folders and files.

```shell
maestro init
```

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

**kill**: Kill a job.

```shell
maestro kill <name>
```

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

**serve**: Create a local server providing a web interface at `http://localhost:<port>`.

```shell
maestro serve [port] [host]
```

- NOTE: default `port` value is: `6969`.
