from backend.client.siu_client import SiuClient
from backend.interactors.result import Result


class SiuInteractor:
    def __init__(self):
        self.client = SiuClient()

    def create_final_act(self, final):
        self.client.create_act(self._build_act(final))
        return Result()

    def list_subjects(self):
        response = self.client.list_subjects()
        return Result(data=response)

    def correlative_subjects(self, subject_siu_id):
        response = self.client.list_correlatives(subject_siu_id)
        return Result(data=response)

    def correlative_finals(self, final_siu_id):
        subject = self.client.get_subject_from_fina(final_siu_id)
        response = self.client.list_correlatives(subject.materia_id)
        # TODO: endpoint for finals of a student?
        pass

    def finals(self, teacher_siu_id, subject_siu_id):
        response = self.client.list_finals(teacher_siu_id, subject_siu_id)
        return Result(data=response)

    def final(self, final_siu_id, teacher_siu_id):
        response = self.client.get_final(final_siu_id, teacher_siu_id)
        return Result(data=response)

    def list_comissions(self, teacher_siu_id):
        response = self.client.list_comissions(teacher_siu_id)
        return Result(data=response)


    def _build_act(self, final):
        return {}
