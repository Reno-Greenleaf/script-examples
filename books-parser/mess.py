"""
Data in given files is a bit messy.
Extracts raw scholar results to be parsed.
"""
def split(row):
  """ Get raw scholar results. First part should contain query details. """
  part = []

  while len(row):
    if len(row) > 1 and not row[1].startswith('<h3'):
      part.append(row.pop(0))
    else:
      yield part
      part = [row.pop(0)]

def clean(row):
  for field in row:
    if field != '#EANF#':
      yield field