#!/usr/bin/python
import storage
from csv import writer

print "Querying results."
data = storage.get_data()
counter = 0

with open('full.csv', 'w') as next_file:
  print "Filling full.csv"
  csv = writer(next_file)
  csv.writerow(('slice', 'source-file', 'categories', 'identifier', 'type', 'title', 'authoring', 'library', 'year', 'source', 'cited_by', 'popularity'))
  csv.writerows(data)

storage.disconnect()