from datetime import datetime
from unittest import mock

from faker import Faker
from rest_framework import status, serializers
from rest_framework.test import APITestCase

from backend.models import Final
from backend.services.siu_service import SiuService
from ..factories import TeacherFactory, FinalFactory, FinalExamFactory


class FinalTeacherViewsTests(APITestCase):
    def setUp(self) -> None:
        self.teacher = TeacherFactory()
        self.subject_siu_id = Faker().numerify(text='###')
        self.subject_name = Faker().word()

    def test_success(self):
        """
        Should fetch all finals belonging to authenticated teacher and which have the subject_siu_id
        passed by parameter
        """
        list_url = f"/api/finals/"
        self.client.force_authenticate(user=self.teacher.user)

        finals = FinalFactory.create_batch(size=3, teacher=self.teacher, subject_siu_id=self.subject_siu_id)
        other_finals = FinalFactory.create_batch(size=3, teacher=self.teacher, subject_siu_id=self.subject_siu_id + "2")

        response = self.client.get(list_url, data={"subject_siu_id": self.subject_siu_id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(finals))
        self.assertEqual(
            sorted([final['id'] for final in response.data]),
            sorted([final.id for final in finals])
        )

    def test_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        list_url = f"/api/finals/"
        response = self.client.get(list_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail(self):
        """
        Should fetch a final with all its final exams an students data
        """
        self.client.force_authenticate(user=self.teacher.user)

        final = FinalFactory(teacher=self.teacher)
        final_exams = FinalExamFactory.create_batch(size=3, final=final, grade=None)

        url = f"/api/finals/{final.id}/"

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], final.pk)
        self.assertEqual(response.data['date'], serializers.DateTimeField().to_representation(final.date))
        self.assertEqual(len(response.data['final_exams']), len(final_exams))

    def test_detail_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        url = f"/api/finals/1/"
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create(self):
        """
        Should create a final with the passed parameters
        """
        mock_final = {
            "id": 12345678,
            "docente_id": 123456,
            "comision_id": 123,
            "timestamp": 1605652352
        }
        with mock.patch.object(SiuService, "__init__", lambda x: None):
            with mock.patch.object(SiuService, "create_final", lambda a, b, c, d: mock_final):

                final_fields = {
                    'subject_name': self.subject_name,
                    'subject_siu_id': self.subject_siu_id,
                    'timestamp': Faker().unix_time()
                }
                url = f"/api/finals/"

                self.client.force_authenticate(user=self.teacher.user)
                response = self.client.post(url, data=final_fields, format='json')

                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(response.data['subject_name'], final_fields['subject_name'])
                self.assertEqual(response.data['date'], serializers.DateTimeField().to_representation(datetime.utcfromtimestamp(final_fields['timestamp'])))
                self.assertEqual(response.data['status'], Final.Status.OPEN)

    def test_create_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        url = f"/api/finals/"
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_close(self):
        """
        Should close final, passing it's status to Pending Act
        :return:
        """
        self.client.force_authenticate(user=self.teacher.user)

        final = FinalFactory(teacher=self.teacher, status=Final.Status.OPEN)

        url = f"/api/finals/{final.id}/close/"

        response = self.client.post(url, format='json')

        self.assertEqual(response.data['status'], Final.Status.PENDING_ACT)

    def test_close_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        url = f"/api/finals/1/close/"
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_grade(self):
        """
        Should add a grade to a final
        """
        self.client.force_authenticate(user=self.teacher.user)

        final = FinalFactory(teacher=self.teacher, status=Final.Status.PENDING_ACT)
        final_exams = FinalExamFactory.create_batch(size=2, final=final, grade=None)

        grades = {fe.id: Faker().random_int(1, 10) for fe in final_exams}

        url = f"/api/finals/{final.id}/grade/"

        response = self.client.put(url, format='json', data={'grades': grades})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], final.id)
        for fe in response.data['final_exams']:
            self.assertEqual(fe['grade'], grades[fe['id']])

    def test_grade_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        url = f"/api/finals/1/grade/"
        response = self.client.put(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_send_act(self):
        """
        Should pass the status to Act Sent
        """
        self.client.force_authenticate(user=self.teacher.user)

        with mock.patch.object(SiuService, "__init__", lambda x: None):
            with mock.patch.object(SiuService, "create_final_act", lambda x, y: {'result': 'ok'}) as siu_mock:

                final = FinalFactory(teacher=self.teacher, status=Final.Status.PENDING_ACT)

                url = f"/api/finals/{final.id}/send_act/"

                response = self.client.post(url, format='json')

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data['status'], Final.Status.ACT_SENT)

    def test_send_act_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        url = f"/api/finals/1/send_act/"
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
