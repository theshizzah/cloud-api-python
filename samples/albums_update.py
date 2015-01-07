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
### Now update the album twice - once to rename to APITestAlbumTest and once to rename it back.
###

data = {'name': 'APITestAlbumTest'}
eyefi.Albums().update(selected_album, data)

data = {'name': 'APITestAlbum'}
eyefi.Albums().update(selected_album, data)