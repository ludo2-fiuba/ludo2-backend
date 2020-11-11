import requests

from backend.client.client_handler import ClientHandler


class SiuClient:
    SIU_URL = "http://localhost:3000"

    def __init__(self, handler=ClientHandler()):
        self.handler = handler

    def create_act(self, act):
        pass

    def list_subjects(self):
        return self.handler.get(self.SIU_URL + '/materias')

    def get_subject(self, subject_siu_id):
        return {'id': 1, 'name': 'Algoritmos y Programación I'}

    def list_correlatives(self, subject_siu_id):
        return []

    def list_finals(self, teacher_siu_id, subject_siu_id):
        return []

    def create_final(self, teacher_siu_id, subject_siu_id, timestamp):
        return {'id': 1}
        pass

    def get_final(self, final_siu_id, teacher_siu_id):
        return {}

    def list_comissions(self, teacher_siu_id):
        return []
