from subprocess import check_output
from sys import exit

import json
# requires corresponding modules installed
import urllib2
import oauth2
from phonenumbers import parse as parse_phone, format_number, PhoneNumberFormat


class Vendor(object):

  def __init__(self, drupal_id, drupal_path):
    """ Prepare data structure to fill. """

    self.yelp = Yelp()
    self.drupal = Drupal(drupal_path)
    self.drupal_id = drupal_id
    self.yelp_id = ''
    self.phone_number = ''
    self.address = False

  def phone(self):
    """ Get data depending on known phone number. """

    phone_numbers = self.drupal.phone(self.drupal_id)

    if len(phone_numbers) > 0:
      self.phone_number = phone_numbers[0]
      yelp_ids = self.yelp.phone(self.phone_number)
    else:
      print "Phone number unknown."
      exit(1)

    if len(yelp_ids) > 1:
      print "There're more than one vendor with such phone number."
      exit(1)
    elif len(yelp_ids) > 0:
      self.yelp_id = yelp_ids.pop()
    else:
      print "Can't find vendor with such phone in Yelp."
      exit(1)

    return self.phone_number

  def address(self):
    pass


class Drupal(object):

  def __init__(self, path):
    """ Remember path to Drupal installation to use it later. """
    self.path = path

  def locate(self, vendor_id, coordinates = False):
    """ Tuples of known location details. """

    query = 'select {field}_thoroughfare, {field}_postal_code, {field}_country from field_data_{field} where entity_id = {id}'
    formatted_query = query.format(field='field_vendor_address', id=vendor_id)
    values = check_output(['drush', 'sqlq', '-r', self.path, formatted_query])
    decoded = values.decode('utf-8')
    rows = filter(None, decoded.split('\n'))
    fields = []

    for location in rows:
      fields.append(tuple(location.split('\t')))

    return fields

  def phone(self, vendor_id):
    """ List of known phone numbers. """

    query = 'select {field}_value from field_data_{field} where entity_id = {id}'
    formatted_query = query.format(field='field_phone_number', id=vendor_id)
    values = check_output(['drush', 'sqlq', '-r', self.path, formatted_query])
    decoded = values.decode('utf-8')
    rows = filter(None, decoded.split('\n'))

    return rows


class Yelp(object):

  def __init__(self):
    """ Data required for Yelp API requests. """

    self.token = 'rdOvA1CJVTVOQX8SqWiKKIWSJdD7RwAp'
    self.key = 'OUt0ZTXvTad2Py3WUvcQxA'
    self.oauth_token = oauth2.Token(self.token, '8y7sdzXiKftOKL5hnej5IraQyCw')
    self.consumer = oauth2.Consumer(self.key, 'tCOxjMMKsQR57kYIHDl8XHiCLpk')
    self.api = 'https://api.yelp.com/v2/%s?'

  def locate(self, location, coordinates=False):
    """
    Find businesses by location.
    Location details are expected in the following order:
    address, neighborhood, city, state or zip, optional country
    """

    prepared_location = []

    for detail in location:
      prepared_location.append(detail.replace(' ', '+'))

    url_parameter = ','.join(prepared_location)
    url = self.api % 'search'
    parameters = {'location': url_parameter}

    if coordinates:
      parameters['cll'] = ','.join(coordinates)

    response = self._request(url, parameters)
    return self._ids(response)

  def phone(self, phone_number):
    """ Find businesses by phone. """

    parsed_phone = parse_phone(phone_number, 'US')
    prepared_phone = format_number(parsed_phone, PhoneNumberFormat.E164)

    url = self.api % 'phone_search'
    parameters = {'phone': prepared_phone}
    response = self._request(url, parameters)
    print response['businesses'][0]['categories']
    return self._ids(response)

  def _request(self, url, url_parameters):
    """ Connection routine. It's here to prevent repetition. """

    request = oauth2.Request(method='GET', url=url, parameters=url_parameters)
    request.update(
      {
        'oauth_nonce': oauth2.generate_nonce(),
        'oauth_timestamp': oauth2.generate_timestamp(),
        'oauth_token': self.token,
        'oauth_consumer_key': self.key
      }
    )
    request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), self.consumer, self.oauth_token)
    signed_url = request.to_url()
    connection = urllib2.urlopen(signed_url, None)

    try:
        response = json.loads(connection.read())
    finally:
        connection.close()

    return response

  def _ids(self, data):
    """ API provides big pack of data. Only IDs are requred. """

    ids = set()
    businesses = data['businesses']

    for business in businesses:
      ids.add(business['id'])

    return ids
