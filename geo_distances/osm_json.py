import json

_mapping = {
	'addr:housenumber': 'addr_housenumber',
	'addr:street': 'addr_street',
	'amenity': 'amenity',
	'name': 'name',
	'name:ru': 'name_ru',
	'opening_hours': 'opening_hours',
	'phone': 'phone',
	'website': 'website',
	'dispensing': 'dispensing',
	'int_name': 'int_name',
	'name:be': 'name_be',
	'addr:postcode': 'addr_postcode',
	'operator': 'operator',
	'ref': 'ref',
	'wheelchair': 'wheelchair',
	'addr:city': 'addr_city',
	'wikidata': 'wikidata',
	'wikipedia': 'wikipedia',
	'description': 'description',
	'name:en': 'name_en',
	'layer': 'layer',
	'operator:ru': 'operator_ru',
	'pharmacy:category': 'pharmacy_category',
	'contact:website': 'contact_website',
	'email': 'email',
	'level': 'level',
	'contact:phone': 'contact_phone',
	'drive_through': 'drive_through',
	'fixme': 'fixme',
	'operator:be': 'operator_be',
	'name:zh': 'name_zh',
	'addr:housename': 'addr_housename',
	'description:be': 'description_be',
	'description:ru': 'description_ru',
	'source': 'source',
	'office': 'office',
	'entrance': 'entrance',
	'addr:country': 'addr_country',
	'brand': 'brand',
	'contact:email': 'contact_email',
	'shop': 'shop',
	'@id': 'nid'
}

def load(io):
	data = json.load(io)

	for feature in data['features']:
		result = {'lat': None, 'lon': None}
		properties = feature['properties']

		if feature['geometry']['type'] == 'Point':
			result['lat'] = feature['geometry']['coordinates'][0]
			result['lon'] = feature['geometry']['coordinates'][1]

		for key in _mapping:
			new_key = _mapping[key]
			result[new_key] = properties.get(key, '')

		yield result