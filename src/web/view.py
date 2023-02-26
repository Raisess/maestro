import os
from jinja2 import Template

class View:
  def __init__(self, filename: str):
    path = "etc/static" if os.path.isdir("etc/static") else "/usr/local/etc/maestro/static"
    with open(f"{path}/{filename}.html", "r") as html_file:
      self.__html = html_file.read()

  def render(self, params: dict[str, str | int] = {}) -> str:
    template = Template(self.__html)
    return template.render(params)
