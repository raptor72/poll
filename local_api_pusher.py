#!venv/bin/python3

import requests
from rest_framework import status
from requests_kerberos import HTTPKerberosAuth, OPTIONAL


CONTURS = {'D': {'Authorization': 'Explicit user@dev.tech',
                   'Content-Type': 'application/json',
                   'Host': 'http://h1.dev.tech:5642'},
           'I': {'Content-Type': 'application/json',
                   'Host': 'http://h1.int.tech:5642'},
           'LOCAL': {'Content-Type': 'application/json',
                   'Host': '10.10.1.1:5334',
                    }
          }


METHODS = {
    'GET': requests.get,
    'POST': requests.post,
    'PUT': requests.put,
    'DELETE': requests.delete,
}


def send_data_through_api(method, api_path, contur, payload=None):
    message = 'Something went wrong'
    status_code = status.HTTP_400_BAD_REQUEST

    headers = CONTURS[contur]
    kerberos_auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)

    if method in METHODS:
        print(''.join([CONTURS[contur]['Host'], api_path]))
#        response = METHODS[method](url=''.join([CONTURS[contur]['Host'], api_path]), headers=headers, data=payload, auth=kerberos_auth)
        response = METHODS[method](url='http://10.10.1.1:5334' + api_path, headers=headers, data=payload, auth=kerberos_auth)
#        return response.json()
        return response
    return message, status_code
