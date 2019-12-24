from csv import DictWriter
from re import findall, sub
""" CSV with several values altered and populated during writing. """

writer = {
  'csv': False
}

def prepare(opened_file):
  columns = ('title', 'phone', 'address', 'state', 'city', 'postal', 'url', 'full-url', 'url_store_id', 'latitude', 'longitude', 'url-for-id-processing')
  writer['csv'] = DictWriter(opened_file, columns)
  writer['csv'].writeheader()

def writerows(rows):
  updated_rows = []

  for row in rows:
    url = row['url']
    row['full-url'] = url
    row['url-for-id-processing'] = url
    row['url'] = url.replace('http://', '').replace('https://', '')

    name = sub('\W+', '', row['title']).lower()
    lat = str(row['latitude']).replace('.', '')[:9]
    lon = str(row['longitude']).replace('.', '')[:9]
    phone = sub('\W+', '', row['phone']).lower()
    city = sub('\W+', '', row['city']).lower()
    postal = sub('\W+', '', row['postal']).lower()

    row['url_store_id'] = 'mattress_firm_%s_%s_%s_%s_%s_%s' % (name, lat, lon, phone, city, postal)
    updated_rows.append(row)

  writer['csv'].writerows(updated_rows)