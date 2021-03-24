import os

from backend.client.client_handler import ClientHandler


class AuthFiubaClient:
    AUTH_URL = os.environ["AUTH_FIUBA_URL"]
    AUTH_CLIENT_SECRET = os.environ["AUTH_CLIENT_SECRET"]
    AUTH_CLIENT_ID = os.environ["AUTH_CLIENT_ID"]
    AUTH_REDIRECT_URI = os.environ["AUTH_REDIRECT_URI"]

    def __init__(self, handler=ClientHandler()):
        self.handler = handler

    def get_access_token(self, code):
        return self.handler.post(f"{self.AUTH_URL}/token", data=self._token_body(code), headers=self._token_headers())

    def get_userinfo(self, access_token):
        return self.handler.post(f"{self.AUTH_URL}/userinfo", headers=self._uuserinfo_headers(access_token))

    def _token_body(self, code):
        return {
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': self.AUTH_CLIENT_ID,
            'client_secret': self.AUTH_CLIENT_SECRET,
            'redirect_uri': self.AUTH_REDIRECT_URI
        }

    def _token_headers(self):
        return {'Content-Type': 'application/x-www-form-urlencoded'}

    def _uuserinfo_headers(self, access_token):
        return {"Authorization": f"Bearer {access_token}"}
