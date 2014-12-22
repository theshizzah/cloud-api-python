import sys
import os
import logging

# Temporary until real install is setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import eyefi

logging.basicConfig(level=logging.INFO)

eyefi.set_token(eyefi.get_home_token())

###
### API Call is Albums().get() - list all albums for user
###

albumitems = eyefi.Albums().get()

for albumitem in albumitems:
    print str(albumitem['id']) + ' ' + albumitem['name']



