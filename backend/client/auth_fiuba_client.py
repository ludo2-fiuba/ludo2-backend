import os

from backend.client.client_handler import ClientHandler


class AuthFiubaClient:
    AUTH_URL = os.environ.get("AUTH_FIUBA_URL")
    AUTH_CLIENT_SECRET = os.environ.get("AUTH_CLIENT_SECRET")
    AUTH_CLIENT_ID = os.environ.get("AUTH_CLIENT_ID")
    AUTH_REDIRECT_URI = os.environ.get("AUTH_REDIRECT_URI")

    def __init__(self, handler=ClientHandler()):
        self.handler = handler

    def get_access_token(self, code, redirect_uri):
        return self.handler.post(f"{self.AUTH_URL}/token", data=self._token_body(code, redirect_uri), headers=self._token_headers())

    def get_userinfo(self, access_token):
        return self.handler.post(f"{self.AUTH_URL}/userinfo", headers=self._userinfo_headers(access_token))

    def _token_body(self, code, redirect_uri):
        return {
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': self.AUTH_CLIENT_ID,
            'client_secret': self.AUTH_CLIENT_SECRET,
            'redirect_uri': redirect_uri
        }

    def _token_headers(self):
        return {'Content-Type': 'application/x-www-form-urlencoded'}

    def _userinfo_headers(self, access_token):
        return {"Authorization": f"Bearer {access_token}"}
