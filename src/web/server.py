import traceback
from flask import Flask, redirect, request

from jobs_manager import JobsManager
from logs_manager import LogsManager
from web.view import View

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def home() -> str:
  view = View("index")
  return view.render({ "jobs": enumerate(JobsManager.List()) })


@app.route("/run", methods = ["POST"])
def run() -> None:
  job_name = request.form.get("job_name")
  job = JobsManager.Load(job_name)
  job.run()
  return redirect("/")


@app.route("/remove", methods = ["POST"])
def remove() -> None:
  job_name = request.form.get("job_name")
  JobsManager.Remove(job_name)
  return redirect("/")


@app.route("/logs", methods = ["GET"])
def logs() -> str:
  job_name = request.args.get("job_name")
  logs = LogsManager.List(job_name)
  all_logs = []
  for log in logs:
    all_logs.extend([(log.filename(), entry) for entry in log.data()])

  view = View("logs")
  return view.render({ "name": job_name, "logs": all_logs })


@app.route("/clear-logs", methods = ["POST"])
def clear_logs() -> None:
  job_name = request.form.get("job_name")
  LogsManager.Clear(job_name)
  return redirect("/")


@app.errorhandler(Exception)
def handle_exception(e: Exception):
  view = View("error")
  return view.render({
    "reason": e.__str__(),
    "stacktrace": "".join(traceback.format_tb(e.__traceback__)),
  })
