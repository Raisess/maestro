import os
import json

class JsonDatabase:
  def __init__(self, path: str):
    self.__path = path

  def write(self, model: str, data: any) -> None:
    with open(self.__fullpath(model), "w") as file:
      file.write(json.dumps(data))

  def write_key(self, model: str, key: str, value: any) -> None:
    if not os.path.isfile(self.__fullpath(model)):
      self.write(model, { f"{key}": value })
      return

    content = self.read(model)
    content[key] = value
    self.write(model, content)

  def read(self, model: str) -> dict[str, any]:
    self.__ensure_model(model)
    with open(self.__fullpath(model), "r") as file:
      content = json.load(file)

    return content

  def read_key(self, model: str, key: str) -> any:
    return self.read(model).get(key)

  def delete(self, model: str) -> None:
    self.__ensure_model(model)
    os.remove(self.__fullpath(model))

  def delete_key(self, model: str, key: str) -> None:
    content = self.read(model)
    content.pop(key)
    self.write(model, content)

  def __ensure_model(self, model: str) -> None:
    if not os.path.isfile(self.__fullpath(model)):
      raise Exception("Model do not exists")

  def __fullpath(self, model: str) -> str:
    return f"{self.__path}/{model}.json"
