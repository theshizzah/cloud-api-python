import time
import urllib2
import sys
import os
import logging

from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps

from StringIO import StringIO

# Temporary until real install is setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import eyefi

logging.basicConfig(level=logging.INFO)

eyefi.set_token(eyefi.get_home_token())

###
### Search for a file named 'warholme.jpg', download it, crop it square, turn it grayscale, colorize it,
### create a mosaic, and upload it as 'warholized.jpg'.
###
### Note that this example uses the Pillow fork of the Python Imaging Library (PIL).
### For instructions (including installation) see: https://pillow.readthedocs.org/
###

### Get the 'warholizeme.jpg' photo
#page_params = {'page': 1, 'per_page': 100}
#search_data = { 'name': 'warholizeme.jpg' }
#fileitems = eyefi.Search().get(data=search_data, params=page_params)['items']

page_params = {'page': 1, 'per_page': 1000}
fileitems = eyefi.Files().get(params=page_params)['items']

for fileitem in fileitems:
    if (fileitem['name'] == 'warholizeme.jpg'):
        url = fileitem['media']
        break

response = urllib2.urlopen(url)
im = Image.open(StringIO(response.read()))

### Crop the photo to a square
width = im.size[0]
height = im.size[1]

box = (0, 0, 0, 0)
if width < height:
    box = (0, (height - width) / 2, width - 1, (height + width) / 2)
else:
    box = ((width - height) / 2, 0, (width + height) / 2, height - 1)

im = im.crop(box)

### Grayscale the photo
grayscale_image = ImageOps.grayscale(im)
blackwhite_image = ImageOps.posterize(grayscale_image, 1)

### Create four colorized photos
yellow_blue_image = ImageOps.colorize(blackwhite_image, (255, 255, 0), (50, 9, 125) )
blue_red_image = ImageOps.colorize(blackwhite_image, (0, 0, 255), (255, 0, 0) )
green_blue_image = ImageOps.colorize(blackwhite_image, (0, 255, 0), (0, 0, 255) )
green_pink_image = ImageOps.colorize(blackwhite_image, (0,114,100), (252,0,116) )

### Create a 2x2 mosaic and normalize the size
x = im.size[0]
y = im.size[1]

blank_image = Image.new("RGB", (x*2, y*2))
blank_image.paste(yellow_blue_image, (0,0))
blank_image.paste(green_blue_image, (x,0))
blank_image.paste(green_pink_image, (0,y))
blank_image.paste(blue_red_image, (x,y))

blank_image.thumbnail( (2048, 2048), Image.ANTIALIAS )

### Save it to disk before uploading
blank_image.save('warholized.jpg', 'JPEG', quality = 75)
upload_files = {'warholized.jpg': open('warholized.jpg', 'rb')}

datetimestampformatted = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(os.path.getmtime('warholized.jpg')))
data = {'date_time_taken': datetimestampformatted}

fileitem = eyefi.Files().create(data=data, files=upload_files)
