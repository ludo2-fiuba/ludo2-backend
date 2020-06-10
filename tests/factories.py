from datetime import timezone

import factory


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
    user = factory.SubFactory(UserFactory, is_student=True)


class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'backend.Teacher'

    legajo = factory.Faker('numerify', text='######')
    user = factory.SubFactory(UserFactory, is_teacher=True)


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'backend.Course'

    subject = factory.Faker('word')
    teacher = factory.SubFactory(TeacherFactory)


class FinalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'backend.Final'

    date = factory.Faker('date_time', tzinfo=timezone.utc)
    course = factory.SubFactory(CourseFactory)


class FinalExamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'backend.FinalExam'

    grade = factory.Faker('random_int', min=0, max=10)
    student = factory.SubFactory(StudentFactory)
    final = factory.SubFactory(FinalFactory)
