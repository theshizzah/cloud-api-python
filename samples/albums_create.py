import sys
import os
import logging

# Temporary until real install is setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import eyefi

logging.basicConfig(level=logging.INFO)

eyefi.set_token(eyefi.get_home_token())

###
### API Call is Albums().create(albumdata) - create an album with the attributes specified in albumdata
### as a dictionary
###

albumdata = {'name': 'APITestAlbum'}
albumitem = eyefi.Albums().create(albumdata)

print 'Album ' + str(albumitem['id']) + ' created with name ' + albumitem['name']
