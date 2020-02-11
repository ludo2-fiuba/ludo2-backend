from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase

import random
from ..factories import StudentFactory, SubjectFactory, SubjectWithCorrelativesFactory, FinalExamFactory


class SubjectTests(APITestCase):
    def setUp(self) -> None:
        self.student_1 = StudentFactory()
        self.student_2 = StudentFactory()
        self.student_3 = StudentFactory()

        self.subject_1 = SubjectWithCorrelativesFactory()
        self.subject_2 = SubjectFactory()

        FinalExamFactory.create_batch(size=3, grade=random.randint(4, 10), student=self.student_1)
        FinalExamFactory.create_batch(size=2, grade=random.randint(1, 3), student=self.student_1)
        FinalExamFactory.create_batch(size=2, student=self.student_2)

    def test_history_with_subjects(self):
        """
        Should return only passing subjects for the logged in user
        """
        self.client.force_authenticate(user=self.student_1)
        url = "/api/subjects/history/"
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_history_empty(self):
        """
        Should return empty if the student has no approved subjects
        """
        self.client.force_authenticate(user=self.student_3)
        url = "/api/subjects/history/"
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_history_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        url = "/api/subjects/history/"
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_correlatives_with_subjects(self):
        """
        Should return correlatives only with subject info
        """
        self.client.force_authenticate(user=self.student_1)
        url = f"/api/subjects/{self.subject_1.id}/correlatives/"
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_correlatives_empty(self):
        """
        Should return nothing if subject has no correlatives
        """
        self.client.force_authenticate(user=self.student_1)
        url = f"/api/subjects/{self.subject_2.id}/correlatives/"
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_correlatives_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        url = f"/api/subjects/{self.subject_2.id}/correlatives/"
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_pending_with_subjects(self):
        """
        Should return only passing subjects for the logged in user
        """
        self.client.force_authenticate(user=self.student_1)
        url = "/api/subjects/pending/"
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_pending_empty(self):
        """
        Should return empty if the student has no pending subjects
        """
        self.client.force_authenticate(user=self.student_3)
        url = "/api/subjects/pending/"
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_pending_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        url = "/api/subjects/pending/"
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
