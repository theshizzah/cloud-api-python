import sys
import os
import logging

# Temporary until real install is setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import eyefi

logging.basicConfig(level=logging.INFO)

eyefi.set_token(eyefi.get_home_token())

###
### API Call is Files().create() - upload a new .jpg file
###

### A timestamp for the photo is required as a data element

data = {'date_time_taken': '2014-12-31T12:00:00+00:00'}

### The SDK requires that a files dictionary be created with the filename as the key and a filehandle to the file
### as the value.  The API has a 100MB limit and the implementation will read the entire file into memory before
### upload.

files = {'APITestFile.jpg': open('APITestFile.jpg','rb')}

fileitem = eyefi.Files().create(data, files)
