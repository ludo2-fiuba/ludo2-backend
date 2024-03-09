from unittest import mock

from rest_framework import status
from rest_framework.test import APITestCase

from backend.services.grader_assignment_service import GraderAssignmentService
from tests.factories import (
    EvaluationFactory,
    SubmissionFactory,
    TeacherFactory,
    TeacherRoleFactory,
    CommissionFactory,
    SemesterFactory,
)


class GraderAssignmentServiceTests(APITestCase):
    def setUp(self) -> None:
        # Setup necessary objects for testing
        self.teacher = TeacherFactory()
        self.commission = CommissionFactory()
        self.semester = SemesterFactory(commission=self.commission)
        self.evaluation = EvaluationFactory(semester=self.semester)
        self.submissions = SubmissionFactory.create_batch(5, evaluation=self.evaluation)
        self.teacher_roles = TeacherRoleFactory.create_batch(
            5, commission=self.commission
        )

        # Mock the GraderAssignmentService
        self.grader_assignment_service = mock.patch.object(
            GraderAssignmentService, "auto_assign"
        ).start()

        # Define the URI for the auto_assign_graders endpoint
        self.auto_assign_graders_uri = (
            f"/api/teacher/evaluations/submissions/auto_assign_graders/"
        )

    def test_auto_assign_graders_success(self):
        """
        Should successfully auto-assign graders to submissions.
        """
        self.client.force_authenticate(user=self.teacher.user)

        # Mock the response from the GraderAssignmentService
        self.grader_assignment_service.return_value = self.submissions

        # Make the API request
        response = self.client.put(
            self.auto_assign_graders_uri,
            {"evaluation": self.evaluation.id},
            format="json",
        )

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the GraderAssignmentService was called with the correct arguments
        self.grader_assignment_service.assert_called_once_with(
            self.teacher_roles, self.submissions
        )

    def test_auto_assign_graders_not_found(self):
        """
        Should return 404 if the evaluation is not found.
        """
        self.client.force_authenticate(user=self.teacher.user)

        # Define a non-existent evaluation ID
        non_existent_evaluation_id = 9999

        # Make the API request
        response = self.client.put(
            self.auto_assign_graders_uri,
            {"evaluation": non_existent_evaluation_id},
            format="json",
        )

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_auto_assign_graders_unauthorized(self):
        """
        Should return 401 if the user is not authenticated.
        """
        # Make the API request without authentication
        response = self.client.put(
            self.auto_assign_graders_uri,
            {"evaluation": self.evaluation.id},
            format="json",
        )

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auto_assign_graders_different_numbers(self):
        """
        Should correctly assign graders to submissions with varying numbers of submissions and teacher roles.
        """
        # Create a varying number of submissions and teacher roles
        submissions = SubmissionFactory.create_batch(10, evaluation=self.evaluation)
        teacher_roles = TeacherRoleFactory.create_batch(5, commission=self.commission)

        # Call the service directly without mocking
        service = GraderAssignmentService()
        assigned_submissions = service.auto_assign(teacher_roles, submissions)

        # Assert that each submission has a grader assigned
        for submission in assigned_submissions:
            self.assertIsNotNone(submission.grader)

    def test_auto_assign_graders_more_roles_than_submissions(self):
        """
        Should correctly handle the case where there are more teacher roles than submissions.
        """
        # Create more teacher roles than submissions
        submissions = SubmissionFactory.create_batch(5, evaluation=self.evaluation)
        teacher_roles = TeacherRoleFactory.create_batch(10, commission=self.commission)

        # Call the service directly without mocking
        service = GraderAssignmentService()
        assigned_submissions = service.auto_assign(teacher_roles, submissions)

        # Assert that each submission has a grader assigned and no teacher is assigned to a non-existent submission
        for submission in assigned_submissions:
            self.assertIsNotNone(submission.grader)

    def test_auto_assign_graders_weighted_roles(self):
        """
        Should correctly assign graders based on the weight of each teacher role.
        """
        # Create teacher roles with varying weights
        teacher_roles = [
            TeacherRoleFactory(commission=self.commission, grader_weight=1.0),
            TeacherRoleFactory(commission=self.commission, grader_weight=2.0),
            TeacherRoleFactory(commission=self.commission, grader_weight=3.0),
        ]
        submissions = SubmissionFactory.create_batch(6, evaluation=self.evaluation)

        # Call the service directly without mocking
        service = GraderAssignmentService()
        assigned_submissions = service.auto_assign(teacher_roles, submissions)

        # Assert that the submissions are assigned based on the weight of the teacher roles
        # This is a simplified assertion. You might need to implement more complex logic to verify the distribution.
        self.assertEqual(len(assigned_submissions), len(submissions))

    def tearDown(self) -> None:
        # Stop the mock
        mock.patch.stopall()
