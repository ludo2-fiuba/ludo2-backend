from rest_framework import status
from rest_framework.test import APITestCase

from ..factories import StudentFactory, TeacherFactory, CourseFactory, FinalFactory


class StudentFinalExamViewsTests(APITestCase):
    def setUp(self) -> None:
        self.student = StudentFactory()
        self.teacher = TeacherFactory()
        self.course = CourseFactory(teacher=self.teacher)

        self.final = FinalFactory(course=self.course)

        self.rendir_uri = "/api/final_exams/rendir/"

    def test_rendir(self):
        """
        Should register that the student took the exam and has a FinalExam for him, the Course and the Final.
        """
        self.client.force_authenticate(user=self.student.user)

        response = self.client.post(self.rendir_uri, {"final": self.final.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['student'], self.student.pk)
        self.assertEqual(response.data['grade'], None)
        self.assertEqual(response.data['final'], self.final.id)

    def test_rendir_twice(self):
        """
        Should fail if student tries to take the same exam twice.
        """
        self.client.force_authenticate(user=self.student.user)
        self.client.post(self.rendir_uri, {"final": self.final.id}, format='json')

        response = self.client.post(self.rendir_uri, {"final": self.final.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_rendir_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        response = self.client.post(self.rendir_uri, {"final": self.final.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_rendir_teacher_logged_in(self):
        """
        Should fail if teacher tries to take an exam
        """
        self.client.force_authenticate(user=self.teacher.user)

        response = self.client.post(self.rendir_uri, {"final": self.final.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rendir_incorrect_validation(self):
        """
        Should fail if student is not properly validated
        """
        pass
