# Overview

The Eyefi Cloud Python SDK is a convenience library used to access the Eyefi Cloud RESTful API.  Notes on
the core data structures for requests and responses can be found in the [cloud-api-doc Github repository]
(https://github.com/eyefi/cloud-api-doc).

The library is installable from PyPI using 'pip install eyefi'.  Alternatively, place eyefi.py in your
PYTHON_PATH and import it using 'import eyefi'.

# Authentication

Eyefi's Cloud API uses the [OAuth 2.0 authorization framework](http://tools.ietf.org/html/rfc6749) 
for simple-but-effective authentication and authorization.

The SDK provides two methods that make working with auth tokens easier.  They are get_hometoken() and set_token().
get_hometoken() will retrieve an auth token from the user's home directory in a file called .ef_password.  The
file should contain a dictionary with the key 'token' as such (replace AUTH_TOKEN with the token received
from the Eyefi Web App):

```JSON
{ "token": "AUTH_TOKEN" }
```

Then, in client code, call set_token() on get_hometoken():

```
eyefi.set_token(eyefi.get_home_token())
```

# SDK General Use

## Requests

Each of the API endpoints has been mapped to a class.  Most classes implement the generic methods (create, get,
update, delete) and will return a NotImplementedError exception if not.  Additionally, some classes have additional
functions to map to class specific API calls.

Each request may take one or more of the following parameters:

### object id

The object id (or just 'id') is the numeric id for the class instance that is being actioned.  For example, in the following, the
object id is the album id because the call is being made to Albums():

```
eyefi.Albums().get(albumid)
```

Note that some of the get() methods can take the id parameter optionally.  If it is specified, one object is
returned.  If not, then all objects are returned.

### referenced object id

The referenced object id (or 'ref id') is the numeric id for the object that is being added or removed to the main object id.
For example, when removing a file from an album, the file id is the referenced object id:

```
eyefi.Albums().remove_file(albumid, fileid)
```

See the sample albums_files_remove.py for a complete example.

### data 

The data element is the dictionary structure containing the key-value pairs that will be passed to the API call.
The details of the data element are not manipulated by the SDK.  See the cloud-api-doc documentation for detailed
information on all of the key-value pairs for each API call.

```
albumdata = {'name': 'APITestAlbum'}
albumitem = eyefi.Albums().create(albumdata)
```

See the sample albums_create.py for a complete example.

### params

Certain API calls that retrieve lists of files support paged responses.  The params item is used to specify which
page and how many items per page.  To specify the page details, pass a dictionary to the API call:

```
page_params = {'page': 1, 'per_page': 100}
response = eyefi.Files().get(params=page_params)
```

Note that the response to paged items is a dictionary with a key for 'total_count' indicating the total
number of possible items and a key for 'items' containing an array of file items.  See the sample files_get.py
for a complete example.

### files

The files object is only used in one case - for eyefi.Files().create() to upload a new file.  In this case, the
files object is a dictionary element containing the file name as the key and an open file handle as the value:

```
data = {'date_time_taken': '2015-01-01T12:00:00+00:00'}
files = {'APITestFile.jpg': open('APITestFile.jpg','rb')}
fileitem = eyefi.Files().create(data, files)
```

See the sample files_create.py for a complete example.

## Responses

For create, get, and update methods the response will be a dicitonary containing the key-value pairs described in
cloud-api-doc.  The delete method typically returns None.

## Classes and Methods Reference

### Albums()

| Method | API URL | id | ref id | data | Sample |
|--------|---------|----|--------|------|--------|
| create | POST ../albums | | | Required | albums_create.py |
| get | GET ../albums/{id} | Optional | | | albums_get.py |
| update | PUT ../albums/{id} | Required | | Required | albums_update.py |
| delete | DELETE ../albums/{id} | Required | | | albums_delete.py |
| add_files | POST ../albums/{id}/files | Required | | Required | albums_files_add.py |
| get_files | GET ../albums/{id}/files | Required | | | albums_files_update.py |
| update_files | PUT ../albums/{id}/files | Required | | Required | albums_files_update.py |
| remove_file | DELETE ../albums/{id}/files | Required | Required | | albums_files_remove.py |

### Events()

| Method | API URL | id | ref id | params | data | files | Sample |
|--------|---------|----|--------|--------|------|-------|--------|
| create | POST ../events | | | | Required - event structure | | |
| get | GET ../events/:id | Optional - event id | | Optional | | | events_get.py |
| update | PUT ../events/:id | Required - event id | | | Required - event structure | | |
| delete | DELETE ../events/:id | Required - event id | | | | | |
| get_files | GET ../events/:id/files | Required  - event id| | | | | |

### Files()

Note that many of the tag methods are based off of the Files class and not the Tags class.

| Method | API URL | id | ref id | params | data | files | Sample |
|--------|---------|----|--------|--------|------|-------|--------|
| create | POST ../files | | | | Required - date_time_taken | Required - filename/file handle | files_create.py |
| get | GET ../files/:id | Optional - file id | | Optional | | | files_get.py |
| delete | DELETE ../files/:id | Required  - file id| | | | | files_delete.py |
| add_tags | POST ../files/:id/files | Required  - file id| | | Required - tag structure  | | files_add_tags.py |
| get_tags | GET ../files/:id/files | Required  - file id| | | | | files_get_tags.py |
| remove_tag | DELETE ../files/:id/files | Required  - file id| Required - tag id | | | | files_remove_tag.py |

### Search() - Ad Hoc Searches

| Method | API URL | id | ref id | params | data | files | Sample |
|--------|---------|----|--------|--------|------|-------|--------|
| get | GET ../search/files |  | | Optional | Required - search structure | | search_files_get.py |

### Search_Saved()

| Method | API URL | id | ref id | params | data | files | Sample |
|--------|---------|----|--------|--------|------|-------|--------|
| create | POST ../search/saved | | | | Required - saved search structure | | search_saved.py |
| get | GET ../search/saved/:id | Optional - saved search id | | | | | search_saved.py |
| update | PUT ../search/saved/:id | Required - saved search id | | | Required - saved search structure | | search_saved.py |
| delete | DELETE ../search/saved/:id | Required - saved searchid | | | | | search_saved.py |
| get_files | GET ../search/saved/:id/files | Required  - saved search id| | Optional | | | search_saved.py |

### Trash()

| Method | API URL | id | ref id | params | data | files | Sample |
|--------|---------|----|--------|--------|------|-------|--------|
| get | GET ../trash |  | | | | | trash.py |
| delete (empty trash) | DELETE ../trash | | | | | | trash.py |
| restore_file | GET ../trash/:id/files | Required  - file id| | | | | trash.py |

## Errors

If an error occurs a RuntimeError exception is thrown and details are provided using the logging subsystem.
Initializing the logging subsystem as follows is a good practice:

```
import logging
logging.basicConfig(level=logging.INFO)
```

## Notes on the samples

The samples are grouped so that there can be a logical flow of create, update, add referenced items, remove
referenced items, and delete.  For Albums, albums_test.sh shows the sequence.  For Files and Tags, it's
files_test.sh.  Saved search is encapsulated in one sample which is search_saved.py.  Similarly, trash.py fully
encapsulates the Trash samples.

Additionally, there are three composite examples that show different classes interacting.  They are:

* folder_uploader.py - upload all JPEG files in current directory and add them to an album named after the directory
* search_tagger.py - execute an ad-hoc search and tag the resulting files
* warholizer.py - download a photo, turn it into a "Warhol" 2x2 colorized mosaic, and upload it

Please note that the convenience sample files_test_create.py and the warholizer.py use the Pillow implementation
of the Python Imaging Library which is not in most standard Python distributions.  See installation instructions 
in either of those samples.

Finally, the samples involving file deletion and Trash manipulation can be more reliable if the Trash is empty 
when the sequence is executed.



