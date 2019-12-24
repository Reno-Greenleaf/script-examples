""" Deal with local data (CSVs and sqlite DB). """

import os, sqlite3
from csv import DictReader, writer, reader
from stores import Stores
from osm_json import load

connection = sqlite3.connect('geo_data.sqlite')
connection.text_factory = str

def fill():
  print "Preparing data from CSV files for further use."

  with open('origins.csv') as origins:
    csv = reader(origins)
    connection.executemany("""
      INSERT INTO origins
      (`code`, `district`, `microdistrict`, `price`, `priceusd`, `pricepersqm`, `addresshouse`, `totalamount`, `separate`, `storeysnumber`, `material`, `squarefootage`, `notes`, `classification`, `constructiondate`, `renovationdate`, `verificationdate`, `marker`)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, csv)
    connection.commit()

  with open('destinations.json') as destinations:
    data = load(destinations)

    connection.executemany("""
      INSERT INTO destinations
      (`addr_housenumber`, `addr_street`, `amenity`, `name`, `name_ru`, `opening_hours`, `phone`, `website`, `dispensing`, `int_name`, `name_be`, `addr_postcode`, `operator`, `ref`, `wheelchair`, `addr_city`, `wikidata`, `wikipedia`, `description`, `name_en`, `layer`, `operator_ru`, `pharmacy_category`, `contact_website`, `email`, `level`, `contact_phone`, `drive_through`, `fixme`, `operator_be`, `name_zh`, `addr_housename`, `description_be`, `description_ru`, `source`, `office`, `entrance`, `addr_country`, `brand`, `contact_email`, `shop`, `nid`, `lat`, `lon`)
      VALUES (:addr_housenumber, :addr_street, :amenity, :name, :name_ru, :opening_hours, :phone, :website, :dispensing, :int_name, :name_be, :addr_postcode, :operator, :ref, :wheelchair, :addr_city, :wikidata, :wikipedia, :description, :name_en, :layer, :operator_ru, :pharmacy_category, :contact_website, :email, :level, :contact_phone, :drive_through, :fixme, :operator_be, :name_zh, :addr_housename, :description_be, :description_ru, :source, :office, :entrance, :addr_country, :brand, :contact_email, :shop, :nid, :lat, :lon)
    """, data)
    connection.commit()

def clean():
  print "Cleaning up."
  connection.execute('DELETE FROM origins')
  connection.execute('DELETE FROM destinations')
  connection.execute('DELETE FROM closest')
  connection.commit()

def count():
  mattress = connection.execute('SELECT COUNT(`id`) FROM origins').next()[0]
  tempur = connection.execute('SELECT COUNT(`nid`) FROM destinations').next()[0]
  print "There're %d origins and %d destinations available." % (mattress, tempur)
  closest = connection.execute('SELECT COUNT(`origin`) FROM closest').next()[0]

  if closest == 0:
    print "Didn't find any closest stores yet."
  elif closest == tempur:
    print "Found all closest stores."
  else:
    print "Found %d closest stores." % closest

def close():
  connection.commit()
  connection.close()

def get_next_origin():
  return Stores(connection.execute("""
    SELECT o.id, o.lat, o.lon FROM origins o
    LEFT JOIN closest AS c ON o.id = c.origin
    WHERE c.origin IS NULL
    LIMIT 1
  """))

def get_addresses_near(origin_id):
  return Stores(connection.execute("""
    SELECT d.nid, d.lat, d.lon FROM origins o
    JOIN destinations AS d
    ON ABS(d.lat - o.lat) <= 0.02 AND ABS(d.lon - o.lon) <= 0.02
    WHERE o.id = :nid
  """, {'nid': origin_id}))

def add_closest(row):
  connection.execute('INSERT INTO closest VALUES (?, ?, ?, ?, ?, ?)', row)
  connection.commit()

def update_map():
  rows = connection.execute("""
    SELECT c.origin, c.readable_distance, c.readable_duration, o.latitude, o.longitude, m.name, m.phone, m.city, m.address, m.cbsa_title, m.url
    FROM closest c
    JOIN mattress_firm AS m ON c.mattress_firm = m.nid
  """)

  with open('mattress_map.csv', 'w') as mattress_map:
    csv = writer(mattress_map)
    csv.writerow(('mattress_firm', 'readable_distance', 'readable_duration', 'latitude', 'longitude', 'name', 'phone', 'city', 'address', 'cbsa_title', 'url'))
    csv.writerows(rows)

def update_tempurpedic_map():
  rows = connection.execute("""
    SELECT c.tempurpedic, c.readable_distance, c.readable_duration, t.latitude, t.longitude, t.phone, t.city, t.address
    FROM closest c
    JOIN tempurpedic AS t ON c.tempurpedic = t.nid
  """)

  with open('tempur_map.csv', 'w') as mattress_map:
    csv = writer(mattress_map)
    csv.writerow(('tempurpedic', 'readable_distance', 'readable_duration', 'latitude', 'longitude', 'phone', 'city', 'address'))
    csv.writerows(rows)

def get_addresses():
  """ Origins lack coorinates. Addresses can be used to add'em with geocoder. """
  return connection.execute("SELECT `id`, `addresshouse` FROM origins WHERE `lat` IS NULL")

def add_coordinates(geodata):
  connection.executemany("UPDATE origins SET lat=:lat, lon=:lon WHERE `id`=:id", geodata)
  connection.commit()