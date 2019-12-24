#!/usr/bin/python
import dataset, storage

print "There're %d files in the dataset." % dataset.total()
print "There're %d files left." % dataset.left()
print "Finished parsing %d files." % dataset.finished()
print "Found %d scholar results." % storage.count()

storage.disconnect()