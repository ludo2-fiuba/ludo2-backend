from rest_framework import status
from rest_framework.test import APITestCase

from ..factories import StudentFactory, TeacherFactory, SubjectFactory, FinalFactory, FinalExamFactory


class FinalTeacherViewsTests(APITestCase):
    def setUp(self) -> None:
        self.teacher = TeacherFactory()
        self.subject = SubjectFactory()

        self.final = FinalFactory(subject=self.subject, teacher=self.teacher)
        self.final_exams = FinalExamFactory.create_batch(size=3, final=self.final, grade=None)

        self.details_url = f"/api/finals/{self.final.id}/details/"

    def test_details(self):
        """
        Should fetch a final with all its final exams an students data
        """
        self.client.force_authenticate(user=self.teacher.user)

        response = self.client.get(self.details_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.final.pk)
        self.assertEqual(response.data['dat'], self.final.date)
        self.assertEqual(len(response.data['final_exams']), len(self.final_exams))

    def test_details_not_logged_in(self):
        """
        Should fail if unauthorized
        """
        response = self.client.post(self.details_uri, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_details_student_logged_in(self):
        """
        Should fail if teacher tries to take an exam
        """
        self.client.force_authenticate(user=self.student.user)

        response = self.client.post(self.details_uri, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

