#!/usr/bin/python
# -*- coding: utf-8 -*-
import geocoder, storage

geodata = []
addresses = storage.get_addresses()

for identifier, address in addresses:
	extended_address = "Минск, %s" % address
	geocoded = geocoder.google(extended_address)
	print address, geocoded.status

	if geocoded.status == 'OK':
		lat, lon = geocoded.latlng
	else:
		continue

	print lat, lon, address
	geodata.append({'lat': lat, 'lon': lon, 'id': identifier})

storage.add_coordinates(geodata)