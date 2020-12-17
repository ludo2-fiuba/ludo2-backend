from backend.client.siu_client import SiuClient
from backend.services.result import Result


class SiuService:
    def __init__(self):
        self.client = SiuClient()

    def create_final_act(self, final): # TODO
        self.client.create_act(self._build_act(final))
        return {'result': 'ok'}

    def list_subjects(self):
        return self.client.list_subjects()

    def get_subject(self, subject_siu_id):
        return self.client.get_subject(subject_siu_id)

    def correlative_subjects(self, subject_siu_id):
        return self.client.list_correlatives(subject_siu_id)

    def correlative_finals(self, final_siu_id): #TODO
        subject = self.client.get_subject_from_fina(final_siu_id)
        response = self.client.list_correlatives(subject.materia_id)
        # TODO: endpoint for finals of a student?
        pass

    def create_final(self, teacher_siu_id, subject_siu_id, timestamp):
        return self.client.create_final(teacher_siu_id, subject_siu_id, timestamp)

    def get_final(self, final_siu_id, teacher_siu_id): #TODO
        response = self.client.get_final(final_siu_id, teacher_siu_id)
        return Result(data=response)

    def list_comissions(self, teacher_siu_id):
        return self.client.list_comissions(teacher_siu_id)

    def _build_act(self, final):
        return {}
