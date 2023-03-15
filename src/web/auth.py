import os
from datetime import timedelta
from flask import session
from uuid import uuid4 as uuid

from database.json_database import JsonDatabase

SESSION_DURATION_MINUTES = 60

class Auth:
  @staticmethod
  def SecretKey() -> str:
    return str(uuid())

  @staticmethod
  def SessionLifetime() -> timedelta:
    return timedelta(minutes=SESSION_DURATION_MINUTES)

  def __init__(self):
    path = "etc" if os.path.isdir("etc") else "/usr/local/etc/maestro"
    self.__auth_db = JsonDatabase(path)

  def login(self, password: str) -> bool:
    if password == self.__auth_db.read("password", "value"):
      session["id"] = str(uuid())
      self.__auth_db.append("session", "id", session["id"])
      return True

    return False

  def is_session_valid(self) -> bool:
    try:
      if session.get("id") == self.__auth_db.read("session", "id"):
        return True

      return False
    except:
      return False
