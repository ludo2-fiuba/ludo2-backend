from backend.models.evaluation_submission import EvaluationSubmission
from backend.models.teacher_role import TeacherRole


class GraderAssignmentService:
    def auto_assign(
        self, teacher_roles: list[TeacherRole], submissions: list[EvaluationSubmission]
    ):
        assigned_graders_count = {"UNASSIGNED": 0}
        for submission in submissions:
            if submission.grader:
                teacher_id = submission.grader.user.id
                assigned_graders_count[teacher_id] = (
                    assigned_graders_count.get(teacher_id, 0) + 1
                )
            else:
                assigned_graders_count["UNASSIGNED"] += 1

        total_submissions = len(submissions)

        total_weight_sum = sum([role.grader_weight for role in teacher_roles])

        sorted_teacher_roles = sorted(
            teacher_roles,
            key=lambda role: role.grader_weight,
            reverse=True,  # Sorting in descending order
        )
        sorted_teacher_weights = [
            (role.teacher.user.id, role.grader_weight) for role in sorted_teacher_roles
        ]

        remaining_ideal_unassigned_submissions = total_submissions
        ideal_assignment_map = {}
        for role in teacher_roles:
            ideal_assignment_map[role.teacher.user.id] = 1.0
            remaining_ideal_unassigned_submissions -= 1.0
            if remaining_ideal_unassigned_submissions <= 0.0:
                # TODO return completed list
                return

        for role in teacher_roles:
            ideal_assignment_map[role.teacher.user.id] += (
                role.grader_weight / total_weight_sum
            ) * remaining_ideal_unassigned_submissions 

