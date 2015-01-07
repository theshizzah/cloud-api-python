import fnmatch
import sys
import os
import logging
import time

# Temporary until real install is setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import eyefi

logging.basicConfig(level=logging.INFO)

eyefi.set_token(eyefi.get_home_token())

###
### This is a small folder uploader.  It will get a list of .jpg files in the current directory, upload them,
### create an album named after the parent directory, and add the photos to the new album.
###

### Get list of files in current directory (case insensitive *.jpg))

fileitems = fnmatch.filter(os.listdir(os.getcwd()), '*.[Jj][Pp][Gg]')

### Find our parent directory name for the Album

albumname = os.path.basename(os.path.abspath(os.getcwd()))

### Create the album

albumresponse = eyefi.Albums().create({'name': albumname})
albumid = albumresponse['id']
if (albumid == None):
    print 'Album ' + albumname + ' failed to create.'
    exit(-1)

print 'Created Album ' + albumname

### Upload the photos and attach them to the album

for fileitem in fileitems:
    ### Get the file modified time and use as date_time_taken..
    datetimestampformatted = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(os.path.getmtime(fileitem)))
    data = {'date_time_taken': datetimestampformatted}

    files = {fileitem: open(fileitem,'rb')}

    fileresponse = eyefi.Files().create(data, files)

    fileid = fileresponse['id']
    if (fileid == None):
        print 'File ' + fileitem + ' failed to upload properly.'
        exit(-1)
    else:
        ### add_files expects an array of files
        eyefi.Albums().add_files(albumid, [ {'id': fileid} ])

        print 'Uploaded ' + fileitem

