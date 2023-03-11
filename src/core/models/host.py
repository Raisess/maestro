import os
import socket

class Host:
  def __init__(self):
    self.__name = socket.gethostname()
    self.__ip = socket.gethostbyname(self.__name)
    self.__os = os.name
    self.__username = os.getlogin()
    self.__cpu_count = os.cpu_count() or 0

  def get_name(self) -> str:
    return self.__name

  def get_ip(self) -> str:
    return self.__ip

  def get_os(self) -> str:
    return self.__os

  def get_username(self) -> str:
    return self.__username

  def get_cpu_count(self) -> int:
    return self.__cpu_count
