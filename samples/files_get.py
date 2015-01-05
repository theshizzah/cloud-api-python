import sys
import os
import logging

import urllib

# Temporary until real install is setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import eyefi

logging.basicConfig(level=logging.INFO)

eyefi.set_token(eyefi.get_home_token())

###
### API Call is Files().get() - list all files for user
### Note that Files().get() supports paging and so will return an 'items' dictionary entry with the array of files.
###

page_params = {'page': 1, 'per_page': 100}
fileitems = eyefi.Files().get(params=page_params)['items']

for fileitem in fileitems:
    if (fileitem['name'] == 'APITestFile.jpg'):
        fileurl = fileitem['media']
        break

###
### The 'media' url on a file object is sufficient to download the file
###

urllib.urlretrieve(fileurl, 'APITestFileDownloaded.jpg')



