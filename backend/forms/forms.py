from django import forms
from django.contrib.auth.forms import UserCreationForm

from backend.models import User


class StaffCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'dni', 'first_name', 'last_name', 'password1', 'password2', 'groups', 'is_staff')

    def __init__(self, *args, **kwargs):
        super(StaffCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save()
        user.is_staff = True
        if commit:
            user.save()
        return user


class RegisterForm(forms.Form):
    # name = forms.CharField(label='Your name')
    pass

