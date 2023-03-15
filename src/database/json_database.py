import os
import json

class JsonDatabase:
  def __init__(self, path: str):
    self.__path = path

  def append(self, model: str, key: str, data: dict) -> None:
    if not os.path.isfile(self.__fullpath(model)):
      self.__write(model, {})

    content = self.read_batch(model)
    content[key] = data
    self.__write(model, content)

  def read(self, model: str, key: str) -> dict | None:
    return self.read_batch(model).get(key)

  def read_batch(self, model: str) -> dict[str, dict]:
    with open(self.__fullpath(model), "r") as file:
      content = json.load(file)

    return content

  def delete(self, model: str, key: str) -> None:
    content = self.read_batch(model)
    content.pop(key)
    self.__write(model, content)

  def __write(self, model: str, data: dict) -> None:
    with open(self.__fullpath(model), "w") as file:
      file.write(json.dumps(data))

  def __fullpath(self, model: str) -> str:
    return f"{self.__path}/{model}.json"
