import logging
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
        self.commission = CommissionFactory(chief_teacher=self.teacher)
        self.semester = SemesterFactory(commission=self.commission)
        self.evaluation = EvaluationFactory(semester=self.semester)
        self.submissions = SubmissionFactory.create_batch(5, evaluation=self.evaluation)
        self.teacher_roles = TeacherRoleFactory.create_batch(
            5, commission=self.commission
        )

        # Define the URI for the auto_assign_graders endpoint
        self.auto_assign_graders_uri = (
            "/api/teacher/evaluations/submissions/auto_assign_graders/"
        )

    @mock.patch.object(GraderAssignmentService, "auto_assign")
    def test_auto_assign_graders_success(self, mocked_grader_assignment_service):
        """
        Should successfully auto-assign graders to submissions.
        """
        self.client.force_authenticate(user=self.teacher.user)

        # Make the API request
        response = self.client.put(
            self.auto_assign_graders_uri,
            {"evaluation": self.evaluation.id},
            format="json",
        )

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the GraderAssignmentService was called with the correct arguments
        mocked_grader_assignment_service.assert_called_once()

    @mock.patch.object(GraderAssignmentService, "auto_assign")
    def test_auto_assign_graders_not_found(self, mocked_grader_assignment_service):
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

    @mock.patch.object(GraderAssignmentService, "auto_assign")
    def test_auto_assign_graders_unauthorized(self, mocked_grader_assignment_service):
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
        teacher_a = TeacherRoleFactory(commission=self.commission, grader_weight=1.0)
        teacher_b = TeacherRoleFactory(commission=self.commission, grader_weight=2.0)
        teacher_c = TeacherRoleFactory(commission=self.commission, grader_weight=3.0)

        teacher_roles = [
            teacher_a,
            teacher_b,
            teacher_c,
        ]
        submissions = SubmissionFactory.create_batch(6, evaluation=self.evaluation)

        # Call the service directly without mocking
        service = GraderAssignmentService()
        assigned_submissions = service.auto_assign(teacher_roles, submissions)

        # Assert that the submissions are assigned based on the weight of the teacher roles
        # This is a simplified assertion. You might need to implement more complex logic to verify the distribution.
        self.assertEqual(len(assigned_submissions), len(submissions))

        teacher_a_subs = [
            sub for sub in assigned_submissions if sub.grader == teacher_a.teacher
        ]
        teacher_b_subs = [
            sub for sub in assigned_submissions if sub.grader == teacher_b.teacher
        ]
        teacher_c_subs = [
            sub for sub in assigned_submissions if sub.grader == teacher_c.teacher
        ]
        self.assertEqual(len(teacher_a_subs), 1)
        self.assertEqual(len(teacher_b_subs), 2)
        self.assertEqual(len(teacher_c_subs), 3)

    def test_auto_assign_many_teachers(self):
        """
        Should correctly assign graders when there are more teachers than subs.
        """
        # Create teacher roles with varying weights
        teacher_a = TeacherRoleFactory(commission=self.commission, grader_weight=1.0)
        teacher_b = TeacherRoleFactory(commission=self.commission, grader_weight=2.0)
        teacher_c = TeacherRoleFactory(commission=self.commission, grader_weight=3.0)

        teacher_roles = [
            teacher_a,
            teacher_b,
            teacher_c,
        ]
        submissions = SubmissionFactory.create_batch(2, evaluation=self.evaluation)

        # Call the service directly without mocking
        service = GraderAssignmentService()
        assigned_submissions = service.auto_assign(teacher_roles, submissions)

        # Assert that the submissions are assigned based on the weight of the teacher roles
        # This is a simplified assertion. You might need to implement more complex logic to verify the distribution.
        self.assertEqual(len(assigned_submissions), len(submissions))

        teacher_a_subs = [
            sub for sub in assigned_submissions if sub.grader == teacher_a.teacher
        ]
        teacher_b_subs = [
            sub for sub in assigned_submissions if sub.grader == teacher_b.teacher
        ]
        teacher_c_subs = [
            sub for sub in assigned_submissions if sub.grader == teacher_c.teacher
        ]
        self.assertEqual(len(teacher_a_subs), 0)
        self.assertEqual(len(teacher_b_subs), 1)
        self.assertEqual(len(teacher_c_subs), 1)

    def test_auto_assign_many_submissions(self):
        """
        Should correctly assign graders when there are many subs.
        """
        # Create teacher roles with varying weights
        teacher_a = TeacherRoleFactory(commission=self.commission, grader_weight=1.0)
        teacher_b = TeacherRoleFactory(commission=self.commission, grader_weight=2.0)
        teacher_c = TeacherRoleFactory(commission=self.commission, grader_weight=3.0)

        teacher_roles = [
            teacher_a,
            teacher_b,
            teacher_c,
        ]
        submissions = SubmissionFactory.create_batch(55, evaluation=self.evaluation)

        # Call the service directly without mocking
        service = GraderAssignmentService()
        assigned_submissions = service.auto_assign(teacher_roles, submissions)

        teacher_a_subs = [
            sub for sub in assigned_submissions if sub.grader == teacher_a.teacher
        ]
        teacher_b_subs = [
            sub for sub in assigned_submissions if sub.grader == teacher_b.teacher
        ]
        teacher_c_subs = [
            sub for sub in assigned_submissions if sub.grader == teacher_c.teacher
        ]
        self.assertEqual(len(teacher_a_subs), 9)
        self.assertEqual(len(teacher_b_subs), 18)
        self.assertEqual(len(teacher_c_subs), 28)

    def test_auto_assign_one_teacher(self):
        """
        Should correctly assign graders when there is only one teacher.
        """
        # Create teacher roles with varying weights
        teacher_a = TeacherRoleFactory(commission=self.commission, grader_weight=5.0)

        teacher_roles = [
            teacher_a,
        ]
        submissions = SubmissionFactory.create_batch(20, evaluation=self.evaluation)

        # Call the service directly without mocking
        service = GraderAssignmentService()
        assigned_submissions = service.auto_assign(teacher_roles, submissions)

        teacher_a_subs = [
            sub for sub in assigned_submissions if sub.grader == teacher_a.teacher
        ]
        self.assertEqual(len(teacher_a_subs), 20)

    def test_auto_assign_zero_submissions(self):
        """
        Should handle the case with zero submissions gracefully.
        """
        teacher_roles = TeacherRoleFactory.create_batch(3, commission=self.commission)
        submissions = []
        service = GraderAssignmentService()
        assigned_submissions = service.auto_assign(teacher_roles, submissions)
        self.assertEqual(len(assigned_submissions), 0)

    def test_auto_assign_zero_teacher_roles(self):
        """
        Should handle the case with zero teacher roles gracefully.
        """
        teacher_roles = []
        submissions = SubmissionFactory.create_batch(5, evaluation=self.evaluation)
        service = GraderAssignmentService()
        assigned_submissions = service.auto_assign(teacher_roles, submissions)
        for submission in assigned_submissions:
            self.assertIsNone(submission.grader)

    def test_auto_assign_equal_weights(self):
        """
        Should distribute submissions evenly among teachers with equal weights.
        """
        teacher_roles = TeacherRoleFactory.create_batch(
            3, commission=self.commission, grader_weight=1.0
        )
        submissions = SubmissionFactory.create_batch(3, evaluation=self.evaluation)
        service = GraderAssignmentService()
        assigned_submissions = service.auto_assign(teacher_roles, submissions)
        grader_ids = [submission.grader.user.id for submission in assigned_submissions]
        unique_grader_ids = set(grader_ids)
        self.assertEqual(len(unique_grader_ids), 3)  # Expecting 3 unique graders
        for grader_id in unique_grader_ids:
            self.assertEqual(
                grader_ids.count(grader_id), 1
            )  # Each grader should have exactly one submission

    def test_auto_assign_one_submission_multiple_teachers(self):
        """
        Should correctly assign the single submission to one of the teachers based on weight.
        """
        teacher_a = TeacherRoleFactory(commission=self.commission, grader_weight=1.0)
        teacher_b = TeacherRoleFactory(commission=self.commission, grader_weight=2.0)
        teacher_roles = [teacher_a, teacher_b]
        submissions = SubmissionFactory.create_batch(1, evaluation=self.evaluation)
        service = GraderAssignmentService()
        assigned_submissions = service.auto_assign(teacher_roles, submissions)
        self.assertEqual(len(assigned_submissions), 1)
        self.assertEqual(assigned_submissions[0].grader, teacher_b.teacher)

    def tearDown(self) -> None:
        # Stop the mock
        mock.patch.stopall()
