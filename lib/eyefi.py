import logging
import os
import json
import urllib
import urllib2
from uuid import uuid4

###
### Globals
###

API_PREFIX = 'https://api.eyefi.com/3/'
AUTH_TOKEN = None

def get_home_token():
    ###
    ### Utility function - looks for file called .ef_password in user's home directory.  File should
    ### contain JSON that has an entry for 'token'.  Example: { 'token': 'ASFBcd34534...' }.
    ###

    # TODO: check for missing file and bad dict
    with open(os.path.expanduser('~/.ef_password')) as auth_file:
        auth_data = json.load(auth_file)
        return(auth_data['token'])

def set_token(token):
    global AUTH_TOKEN
    AUTH_TOKEN = token

def get_authheader():
    global AUTH_TOKEN

    if AUTH_TOKEN != None:
        return 'Bearer ' + AUTH_TOKEN
    else:
        logging.error('Please set an authorization token before making api calls.')

def request_error_handler(response_url, response_code, response_text):
    logging.error('Error in API call: ' + response_url)
    logging.error('Status Code: ' + str(response_code))
    logging.error(response_text)
    raise RuntimeError(response_text)

###
### Eyefi base class
###

class Eyefi(object):
    def exec_request(self, api_params, params=None, data=None, files=None):
        ### Assemble URL.  URL is of form <Api_prefix>/<object>/<opt obj_id>/<opt ref_obj>/<optref_obj_id>
        ### If any parameters are None then skip the rest of the chain

        url = API_PREFIX + api_params['object']
        if 'object_id' in api_params and api_params['object_id'] != None:
            url = url + '/' + str(api_params['object_id'])
            if 'referenced_object' in api_params and api_params['referenced_object'] != None:
                url = url + '/' + api_params['referenced_object']
                if 'referenced_object_id' in api_params and api_params['referenced_object_id'] != None:
                    url = url + '/' + str(api_params['referenced_object_id'])

        ### Some API calls take additional parameters.  Add them to the URL.

        if (params != None):
            url = url + '?' + urllib.urlencode(params)

        logging.info('exec_request ' + api_params['op'] + ' for ' + str(url))

        ### GET handler

        if api_params['op'] == 'get':
            ### For cases where there is a data element for the GET request, add it as URL parameters
            if (data != None):
                url = url + '?' + urllib.urlencode(data)

            request = urllib2.Request(url)
            request.add_header('Authorization', get_authheader())
            response = urllib2.urlopen(request)
            if (response.getcode() != 200):
                request_error_handler(url, response.getcode(), response.read())
            else:
                response_text = response.read()
            response.close()
            return json.loads(response_text)

        ### POST handler (no file upload)

        elif api_params['op'] == 'post' and files == None:
            ### Some of the post calls have no data - add a 'null' json doc in this case so urllib2 will do a post
            if (data == None):
                data = '{}'

            request = urllib2.Request(url, data=json.dumps(data))
            request.add_header('Authorization', get_authheader())
            request.add_header('Content-type', 'application/json')
            response = urllib2.urlopen(request)

            ### If the POST returns 204, it won't have response_text.  Otherwise it should be 200 or 201.
            if (response.getcode() == 204):
                response_text = None
            elif (response.getcode() != 200 and response.getcode() != 201):
                request_error_handler(url, response.getcode(), response.read())
            else:
                response_text = response.read()
            response.close()

            ### Return None if the response_text was empty
            if (response_text != None):
                return json.loads(response_text)
            else:
                return None

        ### POST handler (file upload)

        elif api_params['op'] == 'post' and files != None:
            parts = []
            boundary = 'EFFILEHANDLER' + uuid4().hex + 'EFFILEHANDLER'

            ### Handle fields
            for name, value in data.iteritems():
                parts.extend( [ '--' + boundary,
                                'Content-Disposition: form-data; name="%s"' % name,
                                '',
                                value
                              ]
                            )

            ### Handle files
            for filename, filehandle in files.iteritems():
                parts.extend( [ '--' + boundary,
                                'Content-Disposition: file; name="%s"; filename="%s"' % \
                                (filename, filename),
                                'Content-Type: image/jpeg',
                                '',
                                filehandle.read()
                              ]
                            )

            ### Closing boundary and convert to string
            parts.extend(['--' + boundary + '--'])
            request_body_str = '\r\n'.join(parts)

            ### Process the upload request

            request = urllib2.Request(url)
            request.add_header('Authorization', get_authheader())
            request.add_header('Content-type', 'multipart/form-data; boundary=' + boundary)
            request.add_header('Content-length', len(request_body_str))
            request.add_data(request_body_str)
            response = urllib2.urlopen(request)

            if (response.getcode() != 200 and response.getcode() != 201):
                request_error_handler(url, response.getcode(), response.read())
            else:
                response_text = response.read()
            response.close()
            return json.loads(response_text)

        ### PUT handler

        elif api_params['op'] == 'put':
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            request = urllib2.Request(url, data=json.dumps(data))
            request.add_header('Authorization', get_authheader())
            request.add_header('Content-type', 'application/json')
            request.get_method = lambda: 'PUT'
            response = opener.open(request)

            if (response.getcode() != 200 and response.getcode() != 201):
                request_error_handler(url, response.getcode(), response.read())
            else:
                response_text = response.read()
            response.close()
            return json.loads(response_text)

        ### DELETE handler

        elif api_params['op'] == 'delete':
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            request = urllib2.Request(url)
            request.add_header('Authorization', get_authheader())
            request.get_method = lambda: 'DELETE'
            response = opener.open(request)

            if (response.getcode() != 204):
                request_error_handler(url, response.getcode(), response.read())
            else:
                response_text = response.read()
            response.close()
            return None

        ### Illegal operation

        else:
            raise NotImplementedError(api_params['op'] + ' ' + str(data) + ' ' + str(files))


class Eyefi_Base(Eyefi):
    ###
    ### Methods that apply to all subclasses
    ###

    def __init__(self):
        self.object_name = None

    def create(self, data, files=None):
        return self.exec_request({'op': 'post',
                                  'object': self.object_name},
                                  data=data,
                                  files=files)

    def get(self, id=None, data=None, params=None):
        return self.exec_request({'op': 'get',
                                  'object': self.object_name,
                                  'object_id': id},
                                  data=data,
                                  params=params)

    def update(self, id, data):
        return self.exec_request({'op': 'put',
                                 'object': self.object_name,
                                 'object_id': id},
                                 data=data)

    def delete(self, id=None):
        return self.exec_request({'op': 'delete',
                                  'object': self.object_name,
                                  'object_id': id})

###
### Albums class
###

class Albums(Eyefi_Base):
    def __init__(self):
        self.object_name = 'albums'

    def add_files(self, id, data):
        return self.exec_request({'op': 'post',
                                  'object': self.object_name,
                                  'object_id': id,
                                  'referenced_object': 'files'},
                                  data=data)

    def get_files(self, id):
        return self.exec_request({'op': 'get',
                                  'object': self.object_name,
                                  'object_id': id,
                                  'referenced_object': 'files'})

    def update_files(self, id, data):
        return self.exec_request({'op': 'put',
                                  'object': self.object_name,
                                  'object_id': id,
                                  'referenced_object': 'files'},
                                  data=data)

    def remove_file(self, id, ref_id):
        return self.exec_request({'op': 'delete',
                                  'object': self.object_name,
                                  'object_id': id,
                                  'referenced_object': 'files',
                                  'referenced_object_id': ref_id})

###
### Events class
###

class Events(Eyefi_Base):
    def __init__(self):
        self.object_name = 'events'

    def get_files(self, id):
        return self.exec_request({'op': 'get',
                                  'object': self.object_name,
                                  'object_id': id,
                                  'referenced_object': 'files'})

###
### Files class
###

class Files(Eyefi_Base):
    def __init__(self):
        self.object_name = 'files'

    def update(self, id, data):
        raise NotImplementedError('Files().update()')

    def add_tags(self, id, data):
        return self.exec_request({'op': 'post',
                                  'object': self.object_name,
                                  'object_id': id,
                                  'referenced_object': 'tags'},
                                  data=data)

    def get_tags(self, id):
        return self.exec_request({'op': 'get',
                                  'object': self.object_name,
                                  'object_id': id,
                                  'referenced_object': 'tags'})

    def remove_tag(self, id, ref_id):
        return self.exec_request({'op': 'delete',
                                  'object': self.object_name,
                                  'object_id': id,
                                  'referenced_object': 'tags',
                                  'referenced_object_id': ref_id})

###
### Tags class
###

class Tags(Eyefi_Base):
    def __init__(self):
        self.object_name = 'tags'

    def get_files(self, id):
        return self.exec_request({'op': 'get',
                                  'object': self.object_name,
                                  'object_id': id,
                                  'referenced_object': 'files'})

###
### Search classes
###

class Search(Eyefi_Base):
    def __init__(self):
        self.object_name = 'search/files'

    def create(self, data, files=None):
        raise NotImplementedError('Search().create()')

    def update(self, id, data):
        raise NotImplementedError('Search().update()')

    def delete(self, id):
        raise NotImplementedError('Search().delete()')

class Search_Saved(Eyefi_Base):
    def __init__(self):
        self.object_name = 'search/saved'

    def get_files(self, id, params=None):
        return self.exec_request({'op': 'get',
                                  'object': self.object_name,
                                  'object_id': id,
                                  'referenced_object': 'files'},
                                  params=params)

###
### Trash class
###

class Trash(Eyefi_Base):
    def __init__(self):
        self.object_name = 'trash/files'

    def create(self, data, files=None):
        raise NotImplementedError('Trash().create()')

    def update(self, id, data):
        raise NotImplementedError('Trash().update()')

    def restore_file(self, id):
        return self.exec_request({'op': 'post',
                                  'object': self.object_name,
                                  'object_id': id,
                                  'referenced_object': 'restore'})
