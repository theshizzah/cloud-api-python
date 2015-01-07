import sys
import os
import logging

# Temporary until real install is setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import eyefi

logging.basicConfig(level=logging.INFO)

eyefi.set_token(eyefi.get_home_token())

###
### API Call is Events().get() - list all events for user
###

eventitems = eyefi.Events().get()

for eventitem in eventitems:
    ### If the event name is none, just display the start date
    if (eventitem['name'] == None):
        eventname = eventitem['start_date'][:eventitem['start_date'].find('T')]
    else:
        eventname = eventitem['name']

    print str(eventitem['id']) + ' ' + eventname



