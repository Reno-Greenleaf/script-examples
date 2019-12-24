#!/usr/bin/python
from requests import get, exceptions
from bs4 import BeautifulSoup as bs
from re import findall, sub
from json import loads

""" Visit and use MattressFirm site. """

site = {
  'current page': ''
}

states = set()
regions = set()
stores = set()

def navigate(url):
  while True:
    try:
      response = get(url)
      break
    except exceptions.ConnectionError:
      print "Failed to connect to %s. Retrying." % url

  site['current page'] = bs(response.content, 'html.parser', from_encoding='utf-8')

def parse():
  json = site['current page'].find('script', type='application/ld+json').get_text().encode('utf-8')
  data = loads(json, strict=False)[0]
  address = data.get('address', {})
  geo = data.get('geo', {})

  yield {
    'title': data.get('name', ''),
    'phone': address.get('telephone', ''),
    'address': address.get('streetAddress', ''),
    'state': address.get('addressRegion', ''),
    'city': address.get('addressLocality', ''),
    'postal': address.get('postalCode', ''),
    'url': data.get('url', ''),
    'latitude': geo.get('latitude', ''),
    'longitude': geo.get('longitude', '')
  }

def find_states():
  block = site['current page'].find('div', class_='tlsmap_list')
  links = block.find_all('a')

  for link in links:
    states.add(link['href'])

def find_regions():
  block = site['current page'].find('div', class_='tlsmap_list')
  links = block.find_all('a')

  for link in links:
    regions.add(link['href'])

def find_stores():
  links = site['current page'].find_all('a', class_='rls_citylist_info')

  for link in links:
    stores.add(link['href'])

def list_states():
  for state in states:
    yield state

def list_regions():
  for region in regions:
    yield region

def list_stores():
  for store in stores:
    yield store