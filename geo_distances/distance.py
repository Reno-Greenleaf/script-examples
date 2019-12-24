class Distances(dict):
  """ Deal with data retrieved from distance matrix. """

  def find_fastest(self):
    durations = []

    for element in self['rows'][0]['elements']:

      if 'duration' in element:
        durations.append(element['duration']['value'])
      else:
        durations.append(99999999999)

    fastest = min(durations)
    offset = durations.index(fastest)
    return offset

  def get_distance(self, offset):
    element = self['rows'][0]['elements'][offset]

    if 'distance' in element:
      return (element['distance']['value'], element['distance']['text'], element['duration']['value'], element['duration']['text'])
    else:
      return (0, '', 0, '')

  def get_status(self):
    return self.get('status', 'OK')

  def __len__(self):
    return len(self['rows'][0]['elements'])