#!/usr/bin/python
# -*- coding: utf-8 -*-

from csv import writer, DictReader
from StringIO import StringIO
import requests

from google_api import url, data, extract, temp

csv_page = requests.get('http://162.243.37.150:8080/comparisons/pending', auth=('admin', 'ep'))
pending_file = StringIO(csv_page.text)
pending = DictReader(pending_file)

with open('ratings.csv', 'w') as csv_trends:
  csv_writer = writer(csv_trends)
  csv_writer.writerow(('comparison', 'title', 'start_date', 'end_date', 'trend', 'value'))

  for row in pending:
    trends = row['trends'].split(',')
    interval_start = row['start']
    interval_end = row['end']
    comparison_nid = row['nid']
    request = url(trends, interval_start, interval_end)
    page = request.text
    # page = response.read()
    # page = temp()
    parsed = data(page)
    ratings = extract(parsed, trends, comparison_nid)
    for rating in ratings:
      csv_writer.writerow(rating)