from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator

from backend.models import User


class StaffCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'dni', 'first_name', 'last_name', 'password1', 'password2', 'groups', 'is_staff')

    # or override the __init__ method and set initial=False
    # this is a bit more complicated but less repetitive
    def __init__(self, *args, **kwargs):
        super(StaffCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save()
        user.is_staff = True
        if commit:
            user.save()
        return user


class RegisterForm(forms.Form):
    padron = forms.CharField(max_length=6, validators=[MinLengthValidator(5)], required=True)

    def save(self, student):
        try:
            student.inscripto = True
            student.save()
        except Exception as e:
            error_message = str(e)
            self.add_error(None, error_message)
            raise

        return student
