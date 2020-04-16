from rest_framework import serializers

from backend.models import Subject
from . import FinalSerializer
from ..filters.subject_filter import SubjectFilter


class ApprovedSubjectsByStudentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = Subject.objects.filter(final__finalexam__grade__gte=Subject.PASSING_GRADE,
                                                   final__finalexam__student=self.context['request'].user.id).distinct()
        data = SubjectFilter(data, self._filter_params(self.context['request'])).filter()
        return super(ApprovedSubjectsByStudentListSerializer, self).to_representation(data)

    def _filter_params(self, request):
        return request.query_params


class SubjectSerializer(serializers.ModelSerializer):
    finals = FinalSerializer(source='final_set', many=True)

    class Meta:
        model = Subject
        list_serializer_class = ApprovedSubjectsByStudentListSerializer
        fields = ('id', 'name', 'finals')
