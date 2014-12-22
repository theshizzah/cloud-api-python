import logging
import os
import json

_httplib = None

if not _httplib:
    try:
        import requests
        _httplib = 'requests'
    except ImportError:
        print >>sys.stderr, "Error: The Eyefi Python SDK requires the requests library"

###
### Globals
###

Api_prefix = 'https://api.eyefi.com/3/'
Auth_token = None

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
    global Auth_token
    Auth_token = token

def get_authheaders():
    global Auth_token

    if Auth_token != None:
        return { 'Authorization': 'Bearer ' + Auth_token }
    else:
        logging.error('Please set a authorization token before making api calls.')

def request_error_handler(response):
    logging.error('Error in API call: ' + response.url)
    logging.error('Status Code: ' + str(response.status_code))
    logging.error(response.text)
    raise RuntimeError(response.text)

###
### Eyefi base class
###

class Eyefi(object):
    def exec_request(self, api_params, data=None, files=None):
        logging.info('exec_request: ' + str(api_params))

        ### Assemble URL.  URL is of form <Api_prefix>/<objt>/<opt obj_id>/<opt ref_obj>/<optional ref_obj_id>
        ### If any parameters are None then skip the rest of the chain

        url = Api_prefix + api_params['object']
        if 'object_id' in api_params and api_params['object_id'] != None:
            url = url + '/' + str(api_params['object_id'])
            if 'referenced_object' in api_params and api_params['referenced_object'] != None:
                url = url + '/' + api_params['referenced_object']
                if 'referenced_object_id' in api_params and api_params['referenced_object_id'] != None:
                    url = url + '/' + str(api_params['referenced_object_id'])

        response = None

        if api_params['op'] == 'get':
            logging.info('requests.get: ' + str(url))

            response = requests.get(url, headers=get_authheaders())
            if response.status_code != 200:
                request_error_handler(response)

        elif api_params['op'] == 'post':
            logging.info('requests.post: ' + str(url))

            response = requests.post(url, json=data, files=files, headers=get_authheaders())
            if response.status_code != 200 and response.status_code != 201:
                request_error_handler(response)

        elif api_params['op'] == 'put':
            logging.info('requests.put: ' + str(url))

            response = requests.put(url, json=data, headers=get_authheaders())
            if response.status_code != 200 and response.status_code != 201:
                request_error_handler(response)

        elif api_params['op'] == 'delete':
            logging.info('requests.post: ' + str(url))

            response = requests.delete(url, headers=get_authheaders())
            if response.status_code != 204:
                request_error_handler(response)

        return response

class Eyefi_Base(Eyefi):
    ###
    ### Methods that apply to all subclasses
    ###

    def __init__(self):
        self.object_name = None

    def create(self, data, files=None):
        response = self.exec_request({'op': 'post',
                                      'object': self.object_name},
                                     data,
                                     files)
        return response.json()

    def get(self, id=None):
        response = self.exec_request({'op': 'get',
                                      'object': self.object_name,
                                      'object_id': id})
        return response.json()

    def update(self, id, data):
        response = self.exec_request({'op': 'put',
                                      'object': self.object_name,
                                      'object_id': id},
                                     data)
        return response.json()

    def delete(self, id):
        response = self.exec_request({'op': 'delete',
                                      'object': self.object_name,
                                      'object_id': id})
        return None

###
### Albums class
###

class Albums(Eyefi_Base):
    def __init__(self):
        self.object_name = 'albums'

    def add_files(self, id, data):
        response = self.exec_request({'op': 'post',
                                      'object': self.object_name,
                                      'object_id': id,
                                      'referenced_object': 'files'},
                                     data)
        return response.json()

    def get_files(self, id):
        response = self.exec_request({'op': 'get',
                                      'object': self.object_name,
                                      'object_id': id,
                                      'referenced_object': 'files'})
        return response.json()

    def update_files(self, id, data):
        response = self.exec_request({'op': 'put',
                                      'object': self.object_name,
                                      'object_id': id,
                                      'referenced_object': 'files'},
                                     data)
        return response.json()

    def remove_file(self, id, ref_id):
        response = self.exec_request({'op': 'delete',
                                      'object': self.object_name,
                                      'object_id': id,
                                      'referenced_object': 'files',
                                      'referenced_object_id': ref_id})
        return None

###
### Events class
###

class Events(Eyefi_Base):
    def __init__(self):
        self.object_name = 'events'

    def get_files(self, id):
        response = self.exec_request({'op': 'get',
                                      'object': self.object_name,
                                      'object_id': id,
                                      'referenced_object': 'files'})
        return response.json()

###
### Files class
###

class Files(Eyefi_Base):
    def __init__(self):
        self.object_name = 'files'

    def add_tags(self, id, data):
        response = self.exec_request({'op': 'post',
                                      'object': self.object_name,
                                      'object_id': id,
                                      'referenced_object': 'tags'},
                                     data)
        return response.json()

    def get_tags(self, id):
        response = self.exec_request({'op': 'get',
                                      'object': self.object_name,
                                      'object_id': id,
                                      'referenced_object': 'tags'})
        return response.json()

    def remove_tag(self, id, ref_id):
        response = self.exec_request({'op': 'delete',
                                      'object': self.object_name,
                                      'object_id': id,
                                      'referenced_object': 'tags',
                                      'referenced_object_id': ref_id})
        return None

###
### Tags class
###

class Tags(Eyefi_Base):
    def __init__(self):
        self.object_name = 'tags'

###
### Search class
###

###
### Trash class
###











