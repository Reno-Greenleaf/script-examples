#!/usr/bin/python
import os, storage, dataset

dataset.unmark_all()
storage.disconnect()
os.remove('results.sqlite')
print "Removed previous database."
storage.create()
print "Created new one."
exit()