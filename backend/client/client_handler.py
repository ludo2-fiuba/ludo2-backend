import requests
import logging

from rest_framework import status

from backend.api_exceptions import ErrorCommunicatingWithExternalSourceError


class ClientHandler:
    LOG = logging.getLogger("ClientHandler")

    def get(self, url, params=None, headers=None):
        self.LOG.debug(f"Making GET request to {url} with headers {headers} and params {params}")
        r = self._make_request(url, headers, params, None, requests.get)
        self.LOG.debug(f"Received response with status code {r.status_code} and body {r.text}")
        return r.json()

    def post(self, url, params=None, data=None, headers=None):
        self.LOG.debug(f"Making POST request to {url} with headers {headers}, params {params} and data {data}")
        r = self._make_request(url, headers, params, data, requests.post)
        self.LOG.debug(f"Received response with status code {r.status_code} and body {r.text}")
        return r.json()

    def _make_request(self, url, headers, params, data, method):
        try:
            r = method(url, headers=headers, params=params, data=data, verify=False)
            if not r.ok:
                self.LOG.error(f"Unexpected response from external source with status {r.status_code} and body {r.text}")
                raise ErrorCommunicatingWithExternalSourceError(detail="Invalid response from external source")
            return r
        except requests.exceptions.RequestException as e:
            self.LOG.error(f"An unexpected error occurred, tried performing request but resulted in {e}")
            raise ErrorCommunicatingWithExternalSourceError(detail="Unexpected error when communicating with external source")
