from django.contrib.auth.models import (AbstractUser, UserManager)
from django.core.validators import MinLengthValidator
from django.db import models

from ..validators import validate_dni


class CustomStudentManager(UserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Student(AbstractUser):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    dni = models.CharField(validators=[validate_dni], max_length=9, unique=True)
    username = models.CharField(max_length=30, unique=False, blank=True, default='')
    padron = models.CharField(max_length=6, validators=[MinLengthValidator(5)], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomStudentManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'padron']

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
