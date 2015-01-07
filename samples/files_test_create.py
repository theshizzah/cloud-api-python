import sys
import os
import logging

import urllib
import urllib2

from PIL import Image
from PIL import ImageOps
from StringIO import StringIO

# Temporary until real install is setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import eyefi

logging.basicConfig(level=logging.INFO)

eyefi.set_token(eyefi.get_home_token())

###
### Downloads and creates a test image for use with the files_*.py samples.
### Note that the Eyefi Cloud service won't allow duplicate uploads of photos so this script will download
### the most recent photo in your collection, convert it to grayscale using the Python Imaging Library (PIL)
### and save it as 'APITestFile.jpg'
###
### Note that this example uses the Pillow fork of the Python Imaging Library (PIL).
### For instructions (including installation) see: https://pillow.readthedocs.org/
###

###
### API Call is Files().get() - list all files for user
### Note that Files().get() supports paging and so will return an 'items' dictionary entry with the array of files.
###

page_params = {'page': 1, 'per_page': 100}
fileitems = eyefi.Files().get(params=page_params)['items']
url = fileitems[0]['media']

###
### The 'media' url on a file object is sufficient to download the file
###

response = urllib2.urlopen(url)

im = Image.open(StringIO(response.read()))
im_grayscale = ImageOps.grayscale(im)
im_grayscale.save('APITestFile.jpg')
