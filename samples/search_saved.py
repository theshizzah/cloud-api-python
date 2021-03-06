import sys
import os
import logging
import urllib
import urllib2
import json

# Temporary until real install is setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import eyefi

logging.basicConfig(level=logging.INFO)

eyefi.set_token(eyefi.get_home_token())

###
### API Call is Search_Saved().* - create new saved search, list it, execute it, and delete it
###
### An additional call will be made to the Google maps API to get the lat and long of "My Location".
###

###
### This URL refers to Eye-Fi headquarters.  Use an address near where you took the pictures in your
### photo collection for best results.
###

url = 'https://maps.googleapis.com/maps/api/geocode/json?address=927+N.+Shoreline+Blvd.,+Mountain+View,+CA'
response = urllib2.urlopen(url)
result = json.loads(response.read())['results'][0]

lat_param = result['geometry']['location']['lat']
lon_param = result['geometry']['location']['lng']

###
### Search within 10 miles of this location and save as APITestSavedSearch
###

search_data = { 'name': 'APITestSavedSearch',
                'query': {'geo_lat': lat_param, 'geo_lon': lon_param, 'geo_distance': '5mi' }
              }

eyefi.Search_Saved().create(search_data)

###
### List saved searches
###

searchitems = eyefi.Search_Saved().get()

searchid = None

for searchitem in searchitems:
    if (searchitem['name'] == 'APITestSavedSearch'):
        searchid = searchitem['id']
        break

print 'Found ' + str(searchid)

###
### Execute search - this is also paged
###

page_params = {'page': 1, 'per_page': 100}
fileitems = eyefi.Search_Saved().get_files(searchid, params=page_params)['items']

for fileitem in fileitems:
    print str(fileitem['id']) + ' ' + fileitem['name']

###
### Delete saved search
###

eyefi.Search_Saved().delete(searchid)
