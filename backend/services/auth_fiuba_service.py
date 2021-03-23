from backend.client.auth_fiuba_client import AuthFiubaClient


class AuthFiubaService:
    def __init__(self):
        self.client = AuthFiubaClient()

    def get_token(self, code):
        return self.client.get_access_token(code)

    def userinfo(self, access_token):
        return self.client.get_userinfo(access_token)
