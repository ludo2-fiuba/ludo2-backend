import os

from backend.client.client_handler import ClientHandler


class AuthFiubaClient:
    AUTH_URL = os.environ["AUTH_FIUBA_URL"]

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
            'client_id': 'ed6fdc77-51b0-4828-be5d-37d23d1b6880',
            'client_secret': 'AJh11o6_IWoUKzwEt_CkrS6DGPKSyhcUDpxLZVNJ_aGeuasY0sYq6Jk5PV-HbX5IJwUe26kFLAYBzf3_jUgDbxA',
            'redirect_uri': "https://oauthdebugger.com/debug"
        }

    def _token_headers(self):
        return {'Content-Type': 'application/x-www-form-urlencoded'}

    def _uuserinfo_headers(self, access_token):
        return {"Authorization": f"Bearer {access_token}"}
