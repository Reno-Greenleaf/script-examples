""" Access to geocoder distance matrix. """

from requests import get
from distance import Distances

api_keys = set([
  'AIzaSyBEaTBW09eChwAqQoObGIH4YXYIcu4YhXM',
  'AIzaSyAE4AcPigB1BPEDwSjfE3p_7vXSH7aOx3A',
  'AIzaSyAD83wYhgQTQmwNBEz-q6nz7y4gsTZrpT4',
  'AIzaSyBF5hQ1iGXZ64ii8vULq7Nz2DI8GeHZUCU',
  'AIzaSyDj9GSzfosEG_dJQKwk7HA9avtrkJaq5b8',
  'AIzaSyD1MYhzdCpMiSktLwdgTkepLBjTNvENskA',
  'AIzaSyDZL05RZJ0gIwxGdrXqb6jeBLHggXTtwvM',
  'AIzaSyDcW83VujPTYQ3OZ8Wx49oHPzvEVg5Bi8c',
  'AIzaSyDa2YuhINMWfYSedTcCpIrg8RllXLeES6A',
  # 'AIzaSyAfo_gXJ6U91ZmUzE3FX3mtJk_iUqa9vP0',
  'AIzaSyCSI7xK37xRa8AVItBP_v8YElkViyLpPDo',
  'AIzaSyDiLMgoE5uDtrYVZ9FA5b1qSPyOffz5_ys',
  'AIzaSyBgHkP94nC_WmU1NSfx2B_e64of8XE35wo',
  # 'AIzaSyBMU2ks9NCKSYV0zbzxKIyXk-Yg9E8SDp0',
  'AIzaSyAHZlMkFG8LHGR8t17bA8E8dsas0EgQKPI',
  'AIzaSyCEmRMqQQLbQ3nPxYN6i7p9VmYYYMJHMD8',
  'AIzaSyCl2lZ7UmBfHygyFK5rKTtmfHcnsYo_cAQ'
])
api_key = api_keys.pop()

def get_distances(origin, destinations):
  url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
  params = {
    'origins': str(origin),
    'destinations': str(destinations),
    'key': api_key
  }
  response = get(url, params=params)
  distances = Distances(response.json())
  return distances

def get_new_key():
  new_key = api_keys.pop()
  print "Using key - %s" % new_key
  return new_key