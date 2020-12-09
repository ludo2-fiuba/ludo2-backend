import os

from backend.client.client_handler import ClientHandler


class SiuClient:
    SIU_URL = os.environ["SIU_URL"]

    def __init__(self, handler=ClientHandler()):
        self.handler = handler

    def create_act(self, act):
        pass

    def list_subjects(self, query=""):
        return self.handler.get(self.SIU_URL + '/materias' + query)

    def get_subject(self, subject_siu_id):
        return self.handler.get(f"{self.SIU_URL}/materias/{subject_siu_id}")

    def list_correlatives(self, subject_siu_id):
        subject = self.get_subject(subject_siu_id)
        if not subject['correlativas']:
            return []
        query = "?codigo[]=" + "&codigo[]=".join(subject['correlativas'])
        return self.list_subjects(query)


    def list_finals(self, teacher_siu_id, subject_siu_id):
        return []

    def create_final(self, teacher_siu_id, subject_siu_id, timestamp):
        data = {'materia_id': subject_siu_id, 'timestamp': timestamp}
        return self.handler.post(f"{self.SIU_URL}/docentes/{teacher_siu_id}/finales", data=data)

    def get_final(self, final_siu_id, teacher_siu_id):
        return self.handler.get(f"{self.SIU_URL}/docentes/{teacher_siu_id}/finales/{final_siu_id}")

    def list_comissions(self, teacher_siu_id):
        return self.handler.get(f"{self.SIU_URL}/docentes/{teacher_siu_id}/comisiones?_expand=materia")
