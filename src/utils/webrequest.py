import requests


class UtilWebRequest:

    def __base_request(self, method, headers, parameters, url, body):

        return requests.request(
            method=method,
            headers=headers,
            params=parameters,
            url=url,
            json=body
        )

    def get(self, headers=None, parameters=None, url=None, body=None):
        return self.__base_request("GET", headers, parameters, url, body)

    def post(self, headers=None, parameters=None, url=None, body=None):
        return self.__base_request("POST", headers, parameters, url, body)
