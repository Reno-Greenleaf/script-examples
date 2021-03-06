import mattressfirm
import storage

home = 'https://stores.mattressfirm.com'
print "Searching for state URLs in %s" % home
mattressfirm.navigate(home)
mattressfirm.find_states()

state = mattressfirm.list_states().next()
print "Searching for region URLs in %s" % state
mattressfirm.navigate(state)
mattressfirm.find_regions()

region = mattressfirm.list_regions().next()
print "Searching for store URLs in %s" % region
mattressfirm.navigate(region)
mattressfirm.find_stores()

with open('mattress_firm.csv', 'w') as opened:
  storage.prepare(opened)

  for url in mattressfirm.list_stores():
    mattressfirm.navigate(url)

    try:
      data = mattressfirm.parse()
    except KeyError:
      print "Couldn't get store data from %s." % url

    storage.writerows(data)