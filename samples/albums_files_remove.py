import sys
import os
import logging

# Temporary until real install is setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import eyefi

logging.basicConfig(level=logging.INFO)

eyefi.set_token(eyefi.get_home_token())

###
### First search all the user's albums for the 'APITestAlbum' album so we have an object to work with
###
### A good sequence to run this example is to do albums_create.py first
###

albumitems = eyefi.Albums().get()

for albumitem in albumitems:
    if (albumitem['name'] == 'APITestAlbum'):
        selected_album = albumitem['id']
        break

###
### Now get the photos in the album so there is one to remove.
###

fileitems = eyefi.Albums().get_files(selected_album)['items']
eyefi.Albums().remove_file(selected_album, fileitems[0]['id'])
