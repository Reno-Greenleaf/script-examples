class Stores(list):
  """ One or more stores retrieved from the storage. """
  def __str__(self):
    """ Can be used as URL parameter. """
    lines = []

    for store in self:
      latitude = str(store[1])
      longitude = str(store[2])
      lines.append(latitude + ',' + longitude)

    return '|'.join(lines)

  def __getslice__(self, i, j):
    """ Helpful when amount of stores to process is limited. """
    list_slice = super(Stores, self).__getslice__(i, j)
    return Stores(list_slice)