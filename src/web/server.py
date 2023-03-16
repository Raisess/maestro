import traceback
from flask import Flask, redirect, request

from core.managers.jobs_manager import JobsManager
from core.managers.logs_manager import LogsManager
from core.models.host import Host
from web.auth import Auth
from web.view import View

app = Flask(__name__)
app.secret_key = Auth.SecretKey()
app.permanent_session_lifetime = Auth.SessionLifetime()
auth = Auth()
host = Host()

# --> Login
@app.route("/login", methods = ["GET", "POST"])
def login() -> str:
  failed_try = False
  if request.method == "POST":
    password = request.form.get("password")
    if auth.login(password):
      return redirect("/")

    failed_try = True

  view = View("login")
  return view.render({ "failed_try": failed_try })


# --> Jobs
@app.route("/", methods = ["GET"])
def home() -> str:
  view = View("index")
  return view.render({
    "host": host,
    "jobs": enumerate(JobsManager.List()),
  })


@app.route("/jobs/run", methods = ["POST"])
def run() -> None:
  job_name = request.form.get("job_name")
  job = JobsManager.Load(job_name)
  job.run()
  JobsManager.Save(job)
  return redirect("/")


@app.route("/jobs/kill", methods = ["POST"])
def kill() -> None:
  job_name = request.form.get("job_name")
  job = JobsManager.Load(job_name)
  job.kill()
  JobsManager.Save(job)
  return redirect("/")


@app.route("/jobs/remove", methods = ["POST"])
def remove() -> None:
  job_name = request.form.get("job_name")
  JobsManager.Remove(job_name)
  return redirect("/")


# --> Logs
@app.route("/logs", methods = ["GET"])
def logs() -> str:
  job_name = request.args.get("job_name")
  logs = LogsManager.List(job_name)
  all_logs = []
  for log in logs:
    all_logs.extend([(log.filename(), entry) for entry in log.data()])

  view = View("logs")
  return view.render({
    "host": host,
    "logs": all_logs,
    "name": job_name,
  })


@app.route("/logs/clear", methods = ["POST"])
def clear_logs() -> None:
  job_name = request.form.get("job_name")
  LogsManager.Clear(job_name)
  return redirect("/")


# --> Handlers
@app.before_request
def authentiaction() -> None:
  if request.path != "/login":
    if not auth.is_session_valid():
      return redirect("/login")


@app.errorhandler(Exception)
def handle_exception(e: Exception):
  app.logger.error(e)
  view = View("error")
  return view.render({
    "reason": e.__str__(),
    "stacktrace": "".join(traceback.format_tb(e.__traceback__)),
  })
