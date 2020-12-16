from datetime import timezone

import factory
from faker import Faker

from backend.models import Final


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'backend.User'

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    dni = factory.Faker('numerify', text='########')
    email = factory.Faker('ascii_safe_email')
    password = factory.Faker('password', length=10)


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'backend.Student'

    padron = factory.Faker('numerify', text='######')
    face_encodings = []
    user = factory.SubFactory(UserFactory, is_student=True)


class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'backend.Teacher'

    legajo = factory.Faker('numerify', text='######')
    siu_id = factory.Faker('numerify', text='###')
    face_encodings = []
    user = factory.SubFactory(UserFactory, is_teacher=True)


class FinalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'backend.Final'

    date = factory.Faker('date_time', tzinfo=timezone.utc)
    siu_id = factory.Faker('numerify', text='###')
    subject_name = Faker().word()
    subject_siu_id = factory.Faker('numerify', text='###')
    qrid = Faker().uuid4()
    status = Faker().random_choices(elements=Final.Status, length=1)[0]
    teacher = factory.SubFactory(TeacherFactory)


class FinalExamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'backend.FinalExam'

    grade = factory.Faker('random_int', min=0, max=10)
    student = factory.SubFactory(StudentFactory)
    final = factory.SubFactory(FinalFactory)
