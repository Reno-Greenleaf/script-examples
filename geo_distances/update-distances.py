#!/usr/bin/python

""" Actual distance calculations, can be executed manually, via cron, Jenkins etc. """

import storage, sys, time, distance_matrix
from requests import exceptions

if len(sys.argv) > 1 and sys.argv[1] == 'fresh-start':
  print "Preparing for updated stores."
  storage.clean()
  storage.fill()
  storage.count()
  storage.close()
else:
  print "Getting distances for a bunch of addresses."
  storage.count()

  for x in xrange(700):
    origin = storage.get_next_origin()
    origin_id, origin_lat, origin_lon = origin[0]

    if origin_lat == '' or origin_lon == '':
      storage.add_closest((origin_id, 0, 0, '', 0, ''))
      continue

    destinations = storage.get_addresses_near(origin_id)
    print "Getting pharmacies closest to #%d. There're %d pharmacies near." % (origin_id, len(destinations))

    if len(destinations) == 0:
      storage.add_closest((origin_id, 0, 0, '', 0, ''))
      continue

    order = [destination[0] for destination in destinations]

    try:
      distances = distance_matrix.get_distances(origin, destinations[:99])
    except exceptions.ConnectionError:
      print "Connection error!"
      continue

    status = distances.get_status()

    if status == 'OVER_QUERY_LIMIT':
      print distances['error_message']
      print "Switching API key."
      distance_matrix.api_key = distance_matrix.get_new_key()
      continue
    if status != 'OK':
      print distances['error_message']
      break

    offset = distances.find_fastest()
    tempur_id = order[offset]
    distance, readable_distance, duration, readable_duration = distances.get_distance(offset)
    storage.add_closest((origin_id, tempur_id, distance, readable_distance, duration, readable_duration))
    time.sleep(.2)

  storage.close()