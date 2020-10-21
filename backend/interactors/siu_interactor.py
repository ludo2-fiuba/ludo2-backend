from backend.client.siu_client import SiuClient
from backend.interactors.result import Result


class SiuInteractor:
    def __init__(self):
        self.client = SiuClient()

    def create_final_act(self, final):
        self.client.create_act(self._build_act(final))
        return Result()

    def subjects(self):
        response = self.client.list_subjects()
        return Result(data=response)

    def correlatives(self, subject_siu_id):
        response = self.client.list_correlatives(subject_siu_id)
        return Result(data=response)

    def finals(self, teacher_siu_id):
        response = self.client.list_finals(teacher_siu_id)
        return Result(data=response)

    def final(self, final_siu_id, teacher_siu_id):
        response = self.client.get_final(final_siu_id, teacher_siu_id)
        return Result(data=response)

    def _build_act(self, final):
        return {}
