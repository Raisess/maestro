import json
import os

from flask import Request

PATH = "etc/whitelist.json" if os.path.isfile("etc/whitelist.json") else "/usr/local/etc/maestro/whitelist.json"

class IPWhitelist:
  __List: list[str] = None

  @staticmethod
  def IsValid(ip: str) -> bool:
    IPWhitelist.__Load()
    return True if ip in IPWhitelist.__List else False

  @staticmethod
  def __Load() -> None:
    if not IPWhitelist.__List:
      with open(PATH, "r") as file:
        IPWhitelist.__List = json.load(file)


class Auth:
  @staticmethod
  def Handle(request: Request) -> None:
    if not IPWhitelist.IsValid(request.remote_addr):
      raise Exception(f"Not authorized access try from: {request.remote_addr}")
