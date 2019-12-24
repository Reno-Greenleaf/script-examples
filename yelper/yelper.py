#!/usr/bin/python

from sys import argv
from vendor import Vendor

if len(argv) > 1:
  drupal_id = int(argv[1])

if len(argv) > 2:
  path = argv[2]
else:
  path = '/var/www/fuelwonk'

vendor = Vendor(drupal_id, path)
vendor.phone()
print vendor.yelp_id