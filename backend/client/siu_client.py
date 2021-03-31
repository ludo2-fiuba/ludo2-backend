import os

from backend.api_exceptions import UserTypeMisMatch
from backend.client.client_handler import ClientHandler


class SiuClient:
    SIU_URL = os.environ.get("SIU_URL")
    API_KEY = os.environ.get("SIU_API_KEY")

    def __init__(self, handler=ClientHandler()):
        self.handler = handler

    def create_act(self, final_siu_id, teacher_siu_id, grades):
        data = {"finalId": final_siu_id, "notas": grades}
        return self._post(f"docentes/{teacher_siu_id}/actas", data=data) # TODO: fix no grades only padrones

    def list_subjects(self, filters):
        query = "?" + "&".join(f"{k}={v}" for k, v in filters.items()) if filters else ""
        return self._get(f"materias/{query}")

    def get_subject(self, subject_siu_id):
        return self._get(f"materias/{subject_siu_id}")

    def list_correlatives(self, subject_siu_id):
        subject = self.get_subject(subject_siu_id)
        if not subject['correlativas']:
            return []
        query = "?codigo[]=" + "&codigo[]=".join(subject['correlativas'])
        return self.list_subjects(query)

    def create_final(self, teacher_siu_id, subject_siu_id, timestamp):
        data = {'materia_id': subject_siu_id, 'timestamp': timestamp}
        return self._post(f"docentes/{teacher_siu_id}/finales", data=data)

    def get_final(self, final_siu_id, teacher_siu_id):
        return self._get(f"docentes/{teacher_siu_id}/finales/{final_siu_id}")

    def list_comissions(self, teacher_siu_id):
        return self._get(f"docentes/{teacher_siu_id}/comisiones?_expand=materia")

    def list_departments(self):
        return self._get(f"departamentos")

    def get_student(self, dni):
        result = self._get(f"alumnos/?dni={dni}")
        if len(result) != 1:
            raise UserTypeMisMatch()
        return result[0]

    def get_teacher(self, dni):
        result = self._get(f"docentes/?dni={dni}")
        if len(result) != 1:
            raise UserTypeMisMatch()
        return result[0]

    def _post(self, url, params=None, data=None, headers={}):
        return self.handler.post(f"{self.SIU_URL}/{url}", params, data, self._add_api_key_header(headers))

    def _get(self, url, params=None, headers={}):
        return self.handler.get(f"{self.SIU_URL}/{url}", params, self._add_api_key_header(headers))

    def _add_api_key_header(self, headers):
        return {**headers, **{'api_key': self.API_KEY}}
