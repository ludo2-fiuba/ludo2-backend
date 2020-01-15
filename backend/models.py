from django.contrib.auth.models import (AbstractUser, UserManager)
from django.core.validators import MinLengthValidator
from django.db import models

from .validators import validate_dni


# Create your models here.

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


class Student(AbstractUser):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    dni = models.CharField(validators=[validate_dni], max_length=9, unique=True)
    username = models.CharField(max_length=30, unique=False, blank=True, default='')
    # email = models.EmailField(max_length=255, unique=True)
    padron = models.CharField(max_length=6, validators=[MinLengthValidator], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomStudentManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']


"""
class Subject(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['name']


class Professor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Course(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Final(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FinalExam(models.Model):
    final = models.ForeignKey(Final, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
"""
