from unittest import mock

from rest_framework import status
from rest_framework.test import APITestCase

from backend.services.siu_service import SiuService
from tests.factories import TeacherFactory


class CommissionViewsTests(APITestCase):
    def setUp(self) -> None:
        self.teacher = TeacherFactory()

        self.commissions_uri = "/api/commissions/"

    def test_list(self):
        """
        Should return list of commissions retrieved from the service
        """

        mock_commissions = [{
            'id': 1,
            'name': 'SomeName',
            'teacher_id': 1,
            'subject_id': 1
        }]

        with mock.patch.object(SiuService, "__init__", lambda x: None):
            with mock.patch.object(SiuService, "list_commissions", lambda x, y: mock_commissions):

                self.client.force_authenticate(user=self.teacher.user)
                response = self.client.get(self.commissions_uri, format='json')

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                for commission in mock_commissions:
                    self.assertEqual(response.data[0]['id'], commission['id'])
                    self.assertEqual(response.data[0]['name'], commission['name'])
                    self.assertEqual(response.data[0]['teacher_id'], commission['teacher_id'])
                    self.assertEqual(response.data[0]['subject_id'], commission['subject_id'])

    def test_list_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        response = self.client.get(self.commissions_uri, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
