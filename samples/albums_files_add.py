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

###
### Now grab 3 files to add to the album.  A list of files is stored under the 'items' key returned
### from Files().get()
###

fileitems = eyefi.Files().get()['items']
del fileitems[3:]

eyefi.Albums().add_files(selected_album, fileitems)
