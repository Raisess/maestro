class Log:
  def __init__(self, filename: str, raw_data: str):
    self.__filename = filename
    self.__data = raw_data.strip()

  def filename(self) -> int:
    return self.__filename

  def data(self) -> str:
    return self.__data
