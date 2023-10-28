from rest_framework import serializers

from backend.models import Semester

from .commission_serializer import CommissionSerializer


class SemesterSerializer(serializers.ModelSerializer):
    year_moment = serializers.CharField()
    start_date = serializers.DateTimeField()
    commission = CommissionSerializer()

    class Meta:
        model = Semester
        fields = ('year_moment', 'start_date', 'commission')
