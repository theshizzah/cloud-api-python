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
### This sample executes an ad-hoc search and applies a tag to the results.  Interestingly enough, since the
### saved searches dynamically update as the photo collection updates a saved search will perform almost the
### same function.
###

###
### Tag everything near Disneyland with the tag 'Disneyland'
###

url = 'https://maps.googleapis.com/maps/api/geocode/json?address=Disneyland'
response = urllib2.urlopen(url)
result = json.loads(response.read())['results'][0]

lat_param = result['geometry']['location']['lat']
lon_param = result['geometry']['location']['lng']

###
### Execute ad-hoc search within 10 miles of this location.  Note that Search().get() is also paged similarly
### to Files().get()
###

page_params = {'page': 1, 'per_page': 100}
search_data = { 'has_geodata': True, 'geo_lat': lat_param, 'geo_lon': lon_param, 'geo_distance': '10mi'}

fileitems = eyefi.Search().get(data=search_data, params=page_params)['items']

### Add the tag 'Disneyland' to the files.  Note that we didn't have to create the Disneyland tag first
### and can refer to it by name instead of id.
for fileitem in fileitems:
    eyefi.Files().add_tags(fileitem['id'], {'name': 'Disneyland'})
