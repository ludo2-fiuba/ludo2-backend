from rest_framework import serializers

from backend.models import Subject
from . import FinalSerializer


class ApprovedSubjectsByStudentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(**self._filter_params(self.context["filters"]))
        return super(ApprovedSubjectsByStudentListSerializer, self).to_representation(data)

    def _filter_params(self, filter_params):
        return dict({Subject.ALLOWED_FILTERS[key]: value for key, value in filter_params.items() if key in Subject.ALLOWED_FILTERS})


class SubjectSerializer(serializers.ModelSerializer):
    finals = FinalSerializer(source='final_set', many=True)

    class Meta:
        model = Subject
        list_serializer_class = ApprovedSubjectsByStudentListSerializer
        fields = ('id', 'name', 'finals')
