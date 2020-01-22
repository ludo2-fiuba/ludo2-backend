from rest_framework import serializers

from backend.models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'dni', 'email', 'padron')
