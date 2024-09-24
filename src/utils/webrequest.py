import requests


class UtilWebRequest:

    def __base_request(self, method, headers, parameters, url, payload):

        return requests.request(
            method=method,
            headers=headers,
            params=parameters,
            url=url,
            data=payload
        )

    def get(self, headers=None, parameters=None, url=None, payload=None):
        return self.__base_request("GET", headers, parameters, url, payload)

    def post(self, headers=None, parameters=None, url=None, payload=None):
        return self.__base_request("POST", headers, parameters, url, payload)
