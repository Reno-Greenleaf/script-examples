from re import match

class Store(object):
  def __init__(self, soup):
    self.soup = soup
    self.address_lines = self.soup.find('div', class_='address').find_all('div')
    line = self.address_lines[2].get_text()
    address_parts_found = match(r'(.*?) (\w\w) (\d+)', line)

    if address_parts_found:
      self.address_details = {'city': address_parts_found.group(1), 'state': address_parts_found.group(2), 'postal': address_parts_found.group(3)}

  def title(self):
    return self.soup.a.get_text()

  def phone(self):
    return self.soup.find('a', class_='phone').get_text()

  def address(self):
    return self.address_lines[1].get_text()

  def state(self):
    return self.address_details['state']

  def city(self):
    return self.address_details['city']

  def postal(self):
    return self.address_details['postal']

  def url(self):
    full = self.soup.a['href']
    short = full.replace('http://', '')
    short = short.replace('https://', '')
    return short

  def full_url(self):
    return self.soup.a['href']

  def identifier(self):
    store_url = self.soup.a['href']
    found = match(r'.*?(\d+)\.m\.html', store_url)

    if found:
      return found.group(1)