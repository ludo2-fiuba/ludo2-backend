from unittest import mock

from rest_framework import status
from rest_framework.test import APITestCase

from backend.services.siu_service import SiuService
from tests.factories import TeacherFactory


class ComissionViewsTests(APITestCase):
    def setUp(self) -> None:
        self.teacher = TeacherFactory()

        self.comissions_uri = "/api/comissions/"

    def test_list(self):
        """
        Should return list of comissions retrieved from the service
        """

        mock_comissions = [{
            'id': 1,
            'name': 'SomeName',
            'teacher_id': 1,
            'subject_id': 1
        }]

        with mock.patch.object(SiuService, "__init__", lambda x: None):
            with mock.patch.object(SiuService, "list_comissions", lambda x, y: mock_comissions):

                self.client.force_authenticate(user=self.teacher.user)
                response = self.client.get(self.comissions_uri, format='json')

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                for comission in mock_comissions:
                    self.assertEqual(response.data[0]['id'], comission['id'])
                    self.assertEqual(response.data[0]['name'], comission['name'])
                    self.assertEqual(response.data[0]['teacher_id'], comission['teacher_id'])
                    self.assertEqual(response.data[0]['subject_id'], comission['subject_id'])

    def test_list_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        response = self.client.get(self.comissions_uri, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
