from django import forms

from backend.models import Student


class InscribirForm(forms.Form):
    inscripto = forms.BooleanField(
        required=True,
    )

    def save(self, student):
        try:
            student = Student.objects.get(
                id=student.pk
            )
            student.inscripto = True
            student.save
        except Exception as e:
            error_message = str(e)
            self.add_error(None, error_message)
            raise

        return student
