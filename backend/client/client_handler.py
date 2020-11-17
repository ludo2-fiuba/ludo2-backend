import requests
import logging

from backend.api_exceptions import ErrorCommunicatingWithExternalSourceError


class ClientHandler:
    LOG = logging.getLogger("ClientHandler")

    def get(self, url, params=None, headers=None):
        self.LOG.debug(f"Making GET request to {url} with headers {headers}")
        r = self._make_request(url, headers, params, requests.get)
        self.LOG.debug(f"Received response with status code {r.status_code} and body {r.text}")
        return r.json()

    def post(self, url, data=None, headers=None):
        pass

    def _make_request(self, url, headers, params, method):
        try:
            r = method(url, headers=headers, params=params)
            if not r.ok:
                self.LOG.error(f"Unexpected response from external source with status {r.status_code} and body {r.text}")
                raise ErrorCommunicatingWithExternalSourceError(status_code=r.status_code, detail="Invalid response from eternal source")
            return r
        except requests.exceptions.RequestException as e:
            self.LOG.error(f"An unexpected error ocurred, tried performing request but resulted in {e}")
            raise ErrorCommunicatingWithExternalSourceError(detail="Unexpected error when communicating with external source")
