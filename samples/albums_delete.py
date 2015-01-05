import sys
import os
import logging

# Temporary until real install is setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import eyefi

logging.basicConfig(level=logging.INFO)

eyefi.set_token(eyefi.get_home_token())

###
### First get all albums for a user so we have an object to work with
###
### A good sequence to run this example is to do albums_create.py first.
### This will create an album called 'APITestAlbum' for testing purposes.
###

albumitems = eyefi.Albums().get()

for albumitem in albumitems:
    if (albumitem['name'] == 'APITestAlbum'):
        selected_album = albumitem['id']
        break

eyefi.Albums().delete(selected_album)
