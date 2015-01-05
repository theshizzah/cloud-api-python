import sys
import os
import logging

# Temporary until real install is setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import eyefi

logging.basicConfig(level=logging.INFO)

eyefi.set_token(eyefi.get_home_token())

###
### A runthrough of the lifecycle for the trash.  In earlier examples (files_delete.py) the file 'APITestFile.jpg'
### was deleted - which will move it to the trash.
###
### 1) List the trash contents
### 2) Restore APITestFile.jpg file from the trash
### 3) Delete it again
### 4) Empty the trash
###

###
### List trash and get APITestFile.jpg fileid
###

fileitems = eyefi.Trash().get()

fileid = None

for fileitem in fileitems:
    if (fileitem['name'] == 'APITestFile.jpg'):
        fileid = fileitem['id']

if (fileid == None):
    print 'Please add a file named APITestFile.jpg to your trash first'
    exit(-1)

print 'Found ' + str(fileid)

###
### Restore APITestFile.jpg
###

eyefi.Trash().restore_file(fileid)

###
### Delete it again
###

eyefi.Files().delete(fileid)

###
### Empty the trash
###

eyefi.Trash().delete()

