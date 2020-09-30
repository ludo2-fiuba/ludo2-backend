from backend.client.siu_client import SIUClient
from backend.interactors.result import Result


class SIUInteractor:
    def __init__(self):
        self.client = SIUClient()

    def create_act(self, final):
        self.client.create_act(self._build_act(final))
        return Result()

    def _build_act(self, final):
        return {}
