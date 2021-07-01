from datetime import datetime
from unittest import mock

from faker import Faker
from rest_framework import status, serializers
from rest_framework.test import APITestCase

from backend.client.siu_client import SiuClient
from backend.models import Final
from backend.services.image_validator_service import ImageValidatorService
from backend.services.notification_service import NotificationService
from ..factories import TeacherFactory, FinalFactory, FinalExamFactory


class FinalTeacherViewsTests(APITestCase):
    def setUp(self) -> None:
        self.teacher = TeacherFactory()
        self.subject_siu_id = Faker().numerify(text='###')
        self.subject_name = Faker().word()

    def test_list_success(self):
        """
        Should fetch all finals belonging to authenticated teacher and which have the subject_siu_id
        passed by parameter
        """
        list_url = f"/api/finals/"
        self.client.force_authenticate(user=self.teacher.user)

        finals = FinalFactory.create_batch(size=3, teacher=self.teacher, subject_siu_id=self.subject_siu_id)
        FinalFactory.create_batch(size=3, teacher=self.teacher, subject_siu_id=self.subject_siu_id + "2")

        mock_subject = [{
            "id": 1,
            "codigo": "62.01",
            "nombre": "Física I",
            "departamentoId": 2,
            "correlativas": []
        }]

        with mock.patch.object(SiuClient, "get_subject", return_value=mock_subject):
            response = self.client.get(list_url, {"subject_siu_id": self.subject_siu_id}, format='json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), len(finals))
            self.assertEqual(
                sorted([final['id'] for final in response.data]),
                sorted([final.id for final in finals])
            )

    def test_list_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        list_url = f"/api/finals/"
        response = self.client.get(list_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_success(self):
        """
        Should fetch a final with all its final exams an students data
        """
        self.client.force_authenticate(user=self.teacher.user)

        final = FinalFactory(teacher=self.teacher)
        final_exams = FinalExamFactory.create_batch(size=3, final=final, grade=None)

        url = f"/api/finals/{final.id}/"

        mock_subject = {
            "id": 2,
            "codigo": "62.02",
            "nombre": "Física II",
            "departamentoId": 2,
            "correlativas": ["62.01"]
        }

        mock_correlatives = [{
            "id": 1,
            "codigo": "62.01",
            "nombre": "Física I",
            "departamentoId": 2,
            "correlativas": []
        }]

        with mock.patch.object(SiuClient, "get_subject", return_value=mock_subject):
            with mock.patch.object(SiuClient, "list_subjects", return_value=mock_correlatives):
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

    def test_create_success(self):
        """
        Should create a final with the passed parameters
        """

        self.client.force_authenticate(user=self.teacher.user)
        final_fields = {
            'subject_name': self.subject_name,
            'subject_siu_id': self.subject_siu_id,
            'timestamp': Faker().unix_time()
        }
        url = f"/api/finals/"

        mock_subject = [{
            "id": 1,
            "codigo": "62.01",
            "nombre": "Física I",
            "departamentoId": 2,
            "correlativas": []
        }]

        with mock.patch.object(SiuClient, "get_subject", return_value=mock_subject):
            response = self.client.post(url, data=final_fields, format='json')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['date'], serializers.DateTimeField().to_representation(datetime.utcfromtimestamp(final_fields['timestamp'])))
            self.assertEqual(response.data['status'], Final.Status.DRAFT)

    def test_create_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        url = f"/api/finals/"
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_close_success(self):
        """
        Should close final, passing it's status to Pending Act
        """
        self.client.force_authenticate(user=self.teacher.user)

        final = FinalFactory(teacher=self.teacher, status=Final.Status.OPEN)

        url = f"/api/finals/{final.id}/close/"

        mock_subject = {
            "id": 1,
            "codigo": "62.01",
            "nombre": "Física I",
            "departamentoId": 2,
            "correlatives": []
        }

        with mock.patch.object(SiuClient, "get_subject", return_value=mock_subject):
            response = self.client.post(url, format='json')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['status'], Final.Status.PENDING_ACT)


    def test_close_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        url = f"/api/finals/1/close/"
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_grade_success(self):
        """
        Should add a grade to a final
        """
        self.client.force_authenticate(user=self.teacher.user)

        final = FinalFactory(teacher=self.teacher, status=Final.Status.PENDING_ACT)
        final_exams = FinalExamFactory.create_batch(size=2, final=final, grade=None)

        grades = [{"final_exam_id": fe.id, "grade": Faker().random_int(1, 10)} for fe in final_exams]

        url = f"/api/finals/{final.id}/grade/"

        mock_subject = {
            "id": 1,
            "codigo": "62.01",
            "nombre": "Física I",
            "departamentoId": 2,
            "correlatives": []
        }

        with mock.patch.object(SiuClient, "get_subject", return_value=mock_subject):
            with mock.patch.object(SiuClient, "save_final_grades", return_value={}):
                response = self.client.put(url, format='json', data=grades)

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data['id'], final.id)
                for idx, fe in enumerate(response.data['final_exams']):
                    self.assertEqual(fe['grade'], grades[idx]["grade"])

    def test_grade_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        url = f"/api/finals/1/grade/"
        response = self.client.put(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_send_act_success(self):
        """
        Should pass the status to Act Sent
        """
        self.client.force_authenticate(user=self.teacher.user)

        final = FinalFactory(teacher=self.teacher, status=Final.Status.PENDING_ACT)

        url = f"/api/finals/{final.id}/send_act/"

        mock_subject = {
            "id": 1,
            "codigo": "62.01",
            "nombre": "Física I",
            "departamentoId": 2,
            "correlatives": []
        }

        with mock.patch.object(ImageValidatorService, "validate_identity", return_value=True):
            with mock.patch.object(SiuClient, "create_act", return_value={'id': '123AB00'}):
                with mock.patch.object(NotificationService, "notify_act", return_value=None):
                    with mock.patch.object(SiuClient, "get_subject", return_value=mock_subject):

                        response = self.client.post(url, format='json', data={'image': 'fake_image'})

                        self.assertEqual(response.status_code, status.HTTP_200_OK)
                        self.assertEqual(response.data['status'], Final.Status.ACT_SENT)
                        self.assertEqual(response.data['act'], '123AB00')

    def test_send_act_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        url = f"/api/finals/1/send_act/"
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
