import csv

def csv_iteration(data):
  while True:
    try:
      yield data.next()
    except StopIteration:
      break
    except csv.Error:
      print "Error while reading CSV!"