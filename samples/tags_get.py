import sys
import os
import logging

# Temporary until real install is setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import eyefi

logging.basicConfig(level=logging.INFO)

eyefi.set_token(eyefi.get_home_token())

###
### API Call is Tags().get() - list all tags for user
###

tagitems = eyefi.Tags().get()

for tagitem in tagitems:
    print str(tagitem['id']) + ' ' + tagitem['name']



