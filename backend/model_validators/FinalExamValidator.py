from backend.api_exceptions import ValidationError


class FinalExamValidator:
    def __init__(self, fe):
        self.fe = fe

    def validate(self):
        self.validate_unique_student_final()

    def validate_unique_student_final(self):
        from backend.models import FinalExam
        if FinalExam.objects.filter(final=self.fe.final, student=self.fe.student).exists():
            raise ValidationError(f"FinalExam already exists for final {self.fe.final_id} and student {self.fe.student_id}")
