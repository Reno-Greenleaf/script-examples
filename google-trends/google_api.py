# -*- coding: utf-8 -*-

import requests
from datetime import datetime as date
from re import search, compile as prepare
from json import loads
from csv import writer


def prepare_dates(line):
  unprepared_start, unprepared_end = line.split(' – ')
  start_components = unprepared_start.split(' ')
  end_components = unprepared_end.split(' ')

  if len(start_components) == 3:
    start_month = start_components[0]
    start_day = start_components[1].replace(',', '')
    start_year = start_components[2]

  if len(end_components) == 3:
    end_month = end_components[0]
    end_day = end_components[1].replace(',', '')
    end_year = end_components[2]

  if len(start_components) == 2:
    start_month = start_components[0]
    start_day = start_components[1]
    start_year = end_components[-1]

  if len(end_components) == 2:
    end_month = start_components[0]
    end_day = end_components[0].replace(',', '')
    end_year = end_components[1]

  start_date = '%s-%s-%s' % (start_year, start_month, start_day)
  end_date = '%s-%s-%s' % (end_year, end_month, end_day)

  parsed_start_date = date.strptime(start_date, '%Y-%b-%d')
  parsed_end_date = date.strptime(end_date, '%Y-%b-%d')

  clear_start_date = date.strftime(parsed_start_date, '%Y-%m-%d')
  clear_end_date = date.strftime(parsed_end_date, '%Y-%m-%d')

  return (clear_start_date, clear_end_date)

def url(terms, start, end):
  parsed_start = date.strptime(start, '%d.%m.%Y')
  parsed_end = date.strptime(end, '%d.%m.%Y')
  google_start = date.strftime(parsed_start, '%m/%Y')
  period = (parsed_end.year - parsed_start.year) * 12 + parsed_end.month - parsed_start.month
  google_end = '%dm' % period

  header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36'
  }
  uri = 'http://www.google.com/trends/fetchComponent'
  parameters = {
    'hl': 'en-US',
    'q': ','.join(terms),
    'cid': 'TIMESERIES_GRAPH_0',
    'export': 3,
    'date': '%s %s' % (google_start, google_end)
  }

  result = requests.get(uri, params=parameters)
  # result = Request(uri, urlencode(parameters), header)
  return result

def temp():
  with open('temp.js') as page:
    return page.read()

def data(page):
  js_part = search('"rows"\:(\[\{.*)\}\}\)\;', page).group(1)
  dates = prepare('"v":new Date\(\d+,\d+,\d+\),')
  json_string = dates.sub('', js_part)
  return loads(json_string)

def extract(json, trends, nid):
  for interval in json:
    values = interval[u'c']
    dates = values[0][u'f']
    week = dates.encode('utf-8')

    for i in range(len(trends)):
      start_date, end_date = prepare_dates(week)
      yield (nid, '%s %s' % (week, trends[i]), start_date, end_date, trends[i], values[i+1][u'v'])