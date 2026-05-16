'''Web request utility module.

This module provides a wrapper around the requests library for making
HTTP requests.
'''

import requests


class UtilWebRequest:
    '''Utility class for making web requests.'''

    def __base_request(self, method, headers, parameters, url, payload):
        '''Performs a base HTTP request.

        Args:
            method (str): The HTTP method (e.g., 'GET', 'POST').
            headers (dict): The request headers.
            parameters (dict): The query parameters.
            url (str): The target URL.
            payload (dict or str): The request payload.

        Returns:
            Response: The response object from the requests library.
        '''
        return requests.request(
            method=method,
            headers=headers,
            params=parameters,
            url=url,
            data=payload,
            timeout=30
        )

    def get(self, headers=None, parameters=None, url=None, payload=None):
        '''Performs an HTTP GET request.

        Args:
            headers (dict): The request headers.
            parameters (dict): The query parameters.
            url (str): The target URL.
            payload (dict or str): The request payload.

        Returns:
            Response: The response object.
        '''
        return self.__base_request('GET', headers, parameters, url, payload)

    def post(self, headers=None, parameters=None, url=None, payload=None):
        '''Performs an HTTP POST request.

        Args:
            headers (dict): The request headers.
            parameters (dict): The query parameters.
            url (str): The target URL.
            payload (dict or str): The request payload.

        Returns:
            Response: The response object.
        '''
        return self.__base_request('POST', headers, parameters, url, payload)
