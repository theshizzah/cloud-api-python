import sys
import os
import logging

# Temporary until real install is setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import eyefi

logging.basicConfig(level=logging.INFO)

eyefi.set_token(eyefi.get_home_token())

###
### First search all the user's files for the 'APITestFile' file so we have an object to work with
###
### A good sequence to run this example is to do files_create.py first
###

page_params = {'page': 1, 'per_page': 100}
fileitems = eyefi.Files().get(params=page_params)['items']

for fileitem in fileitems:
    if (fileitem['name'] == 'APITestFile.jpg'):
        fileid = fileitem['id']

if (fileid == None):
    print 'Please add a file named APITestFile.jpg to your library first'
    exit(-1)

###
### List tags on this file
###

tagitems = eyefi.Files().get_tags(fileid)

tagid = None

for tagitem in tagitems:
    if (tagitem['name'] == 'APITestTag'):
        tagid = tagitem['id']

if (tagid == None):
    print 'Please make sure that APITestFile.jpg is tagged with API TestTag first'
    exit(-1)

eyefi.Files().remove_tag(fileid, tagid)

###
### Note that this doesn't remove the tag if it's the last file with that tag so clean it up
###

eyefi.Tags().delete(tagid)
