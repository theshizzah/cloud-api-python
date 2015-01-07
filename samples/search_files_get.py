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
### API Call is Search().get() - list all files meeting search criteria
###
### An additional call will be made to the Google maps API to get the lat and long of "My Location".
###

###
### This URL refers to Eye-Fi headquarters.  Use an address near where you took the pictures in your
### photo collection.
###

url = 'https://maps.googleapis.com/maps/api/geocode/json?address=927+N.+Shoreline+Blvd.,+Mountain+View,+CA'
response = urllib2.urlopen(url)
result = json.loads(response.read())['results'][0]

lat_param = result['geometry']['location']['lat']
lon_param = result['geometry']['location']['lng']

###
### Execute ad-hoc search within 10 miles of this location.  Note that Search().get() is also paged similarly
### to Files().get()
###

page_params = {'page': 1, 'per_page': 100}
search_data = {'geo_lat': lat_param, 'geo_lon': lon_param, 'geo_distance': '10mi'}

fileitems = eyefi.Search().get(data=search_data, params=page_params)['items']

for fileitem in fileitems:
    print str(fileitem['id']) + ' ' + fileitem['name']
