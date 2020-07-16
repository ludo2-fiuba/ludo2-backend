from rest_framework import serializers

from backend.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'dni', 'email', 'image')
