from rest_framework import serializers

from backend.models import CommissionInscription

from .semester_serializer import SemesterSerializer


class CommissionInscriptionSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()
    status = serializers.CharField()

    class Meta:
        model = CommissionInscription
        fields = ('semester', 'status')
