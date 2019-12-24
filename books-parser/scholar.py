from csv import reader

class ResultsMess(object):
  """ Google Scholar search results. """

  def __init__(self, source):
    self.csv = reader(source)

  def __iter__(self):
    return self.__loop()

  def __loop(self):
    for row in self.csv:
      for pack in packs(row): yield Result(pack)


class Result(object):
  """ Google Scholar result to get details from. """

  def __init__(self, pack):
    self.url, self.html, self.title, self.authoring, self.details, self.cited = pack