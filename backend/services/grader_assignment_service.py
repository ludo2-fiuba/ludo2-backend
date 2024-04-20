import logging
from typing import List

from backend.models.evaluation_submission import EvaluationSubmission
from backend.models.teacher_role import TeacherRole
from backend.services.evaluation_submission_service import \
    EvaluationSubmissionService

logger = logging.getLogger(__name__)


class GraderAssignmentService:
    def _log(self, *obj):
        logger.info(f"GraderAssignmentService: {obj}")

    def auto_assign(
        self, teacher_roles: List[TeacherRole], submissions: List[EvaluationSubmission]
    ) -> List[EvaluationSubmission]:
        """
        Assigns graders to submissions by considering teachers' weights.

        It first makes sure each teacher gets at least one submission to grade. Then, it distributes any remaining submissions based on the teachers' weights.

        Args:
            teacher_roles (list[TeacherRole]): A list of TeacherRole objects showing how many submissions each teacher prefers and can grade.
            submissions (list[EvaluationSubmission]): The submissions that need to be graded.

        Note:
            - Any already-assigned graders are LOST.
            - The `grader` attribute of the EvaluationSubmission objects gets updated to reflect the teacher assignment.
            - Assumes `teacher_roles` and `submissions` are populated and each teacher is uniquely identifiable.
        """
        if not teacher_roles:
            self._log(
                "No teacher roles provided. Returning original submissions without any assignments."
            )
            return submissions
        
        for teacher_role in teacher_roles:
            if(teacher_role.grader_weight <= 0):
                teacher_roles.remove(teacher_role)
                print(f'Removed {teacher_role}')

        submissions_service = EvaluationSubmissionService()
        submissions_count = len(submissions)
        teacher_roles_count = len(teacher_roles)

        sorted_teacher_roles = sorted(
            teacher_roles,
            key=lambda role: role.grader_weight,
            reverse=True,  # Sorting in descending order
        )

        self._log(teacher_roles, submissions, sorted_teacher_roles)

        if teacher_roles_count > submissions_count:
            # Handle the case when there are more teacher roles than submissions
            # For simplicity, we can limit the number of teacher roles to the number of submissions
            sorted_teacher_roles = sorted_teacher_roles[:submissions_count]
            teacher_roles_count = submissions_count

        # assign at least one to each
        for submission, teacher_role in zip(
            submissions[:teacher_roles_count], sorted_teacher_roles
        ):
            submissions_service.set_grader(submission, teacher_role.teacher)

        remaining_submissions = submissions[teacher_roles_count:]

        total_weight_sum = sum([role.grader_weight for role in sorted_teacher_roles])

        ideal_assignment_map = {
            role.teacher.user.id: (role.grader_weight / total_weight_sum)
            * submissions_count
            - 1.0  # discount already assigned on each
            for role in sorted_teacher_roles
        }

        self._log(ideal_assignment_map)

        for submission in remaining_submissions:
            assigned_teacher_id = max(
                ideal_assignment_map, key=lambda x: ideal_assignment_map[x]
            )
            teacher = next(
                role.teacher
                for role in sorted_teacher_roles
                if role.teacher.user.id == assigned_teacher_id
            )
            submissions_service.set_grader(submission, teacher)
            ideal_assignment_map[assigned_teacher_id] -= 1

        self._log(f"Final submissions", submissions)
        return submissions
