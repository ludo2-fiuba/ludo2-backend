from unittest import mock

from rest_framework import status
from rest_framework.test import APITestCase

from backend.services.image_validator_service import ImageValidatorService
from ..factories import StudentFactory, TeacherFactory, FinalFactory


class StudentFinalExamViewsTests(APITestCase):
    def setUp(self) -> None:
        self.student = StudentFactory()
        self.teacher = TeacherFactory()

        self.final = FinalFactory(teacher=self.teacher)

        self.take_exam_uri = "/api/final_exams/take_exam/"

    def test_take_exam(self):
        """
        Should register that the student took the exam and has a FinalExam for him, the Course and the Final.
        """
        self.client.force_authenticate(user=self.student.user)

        with mock.patch.object(ImageValidatorService, "validate_identity", lambda x, y: True):
            response = self.client.post(self.take_exam_uri, {"final": self.final.qrid, "photo": 'fake_b64'}, format='json')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['student'], self.student.pk)
            self.assertEqual(response.data['grade'], None)

    def test_take_exam_twice(self):
        """
        Should fail if student tries to take the same exam twice.
        """
        self.client.force_authenticate(user=self.student.user)

        with mock.patch.object(ImageValidatorService, "validate_identity", lambda x, y: True):
            self.client.post(self.take_exam_uri, {"final": self.final.qrid, "photo": 'fake_b64'}, format='json')
            response = self.client.post(self.take_exam_uri, {"final": self.final.qrid, "photo": 'fake_b64'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_take_exam_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        response = self.client.post(self.take_exam_uri, {"final": self.final.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_take_exam_teacher_logged_in(self):
        """
        Should fail if teacher tries to take an exam
        """
        self.client.force_authenticate(user=self.teacher.user)

        response = self.client.post(self.take_exam_uri, {"final": self.final.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_take_exam_incorrect_validation(self):
        """
        Should fail if student is not properly validated
        """
        pass
