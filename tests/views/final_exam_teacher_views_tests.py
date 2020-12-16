from rest_framework import status
from rest_framework.test import APITestCase

from ..factories import StudentFactory, TeacherFactory, FinalFactory, FinalExamFactory


class FinalExamTeacherViewsTests(APITestCase):
    def setUp(self) -> None:
        self.student = StudentFactory()
        self.teacher = TeacherFactory()

        self.final = FinalFactory(teacher=self.teacher)
        self.final_exam = FinalExamFactory(final=self.final, student=self.student, grade=None)

        self.calificar_uri = f"/api/final_exams/{self.final_exam.id}/calificar/"

    def test_calificar(self):
        """
        Should register that the teacher graded the FinalExam and the exam now has a grade
        """
        self.client.force_authenticate(user=self.teacher.user)

        response = self.client.put(self.calificar_uri, {"grade": 7}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student'], self.student.pk)
        self.assertEqual(response.data['grade'], 7)
        self.assertEqual(response.data['final'], self.final.id)

    def test_calificar_invalid_grade(self):
        """
        Should fail indicating that the grade is invalid
        """
        self.client.force_authenticate(user=self.teacher.user)

        response = self.client.put(self.calificar_uri, {"grade": 70}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['grade'][0], "Ensure this value is less than or equal to 10.")

    def test_calificar_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        response = self.client.post(self.calificar_uri, {"final": self.final.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_calificar_student_logged_in(self):
        """
        Should fail if student tries to grade exam
        """
        self.client.force_authenticate(user=self.student.user)

        response = self.client.post(self.calificar_uri, {"final": self.final.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

