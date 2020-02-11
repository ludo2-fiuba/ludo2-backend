from datetime import timezone

import factory


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'backend.Student'

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    dni = factory.Faker('numerify', text='########')
    email = factory.Faker('ascii_safe_email')
    padron = factory.Faker('numerify', text='######')
    password = factory.Faker('password', length=10)


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'backend.Subject'

    name = factory.Faker('word')


class SubjectWithCorrelativesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'backend.Subject'

    name = factory.Faker('word')

    @factory.post_generation
    def correlatives(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for correlative in extracted:
                self.correlatives.add(correlative)
        else:
            for i in range(2):  # TODO check how to pass the size
                self.correlatives.add(SubjectFactory())


class FinalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'backend.Final'

    date = factory.Faker('date_time', tzinfo=timezone.utc)
    subject = factory.SubFactory(SubjectFactory)


class FinalExamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'backend.FinalExam'

    grade = factory.Faker('random_int', min=0, max=10)
    student = factory.SubFactory(StudentFactory)
    final = factory.SubFactory(FinalFactory)
