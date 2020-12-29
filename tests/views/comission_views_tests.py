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

        }]

        with mock.patch.object(SiuService, "__init__", lambda x: None):
            with mock.patch.object(SiuService, "list_comissions", lambda x, y: mock_comissions):

                self.client.force_authenticate(user=self.teacher.user)
                response = self.client.get(self.comissions_uri, format='json')

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data, [{}])

    def test_list_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        response = self.client.get(self.comissions_uri, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
