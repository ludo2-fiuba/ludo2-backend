from rest_framework import serializers

from backend.models import Subject
from . import FinalSerializer


class SubjectSerializer(serializers.ModelSerializer):
    finals = FinalSerializer(source='final_set', many=True)

    class Meta:
        model = Subject
        fields = ('id', 'name', 'finals')
