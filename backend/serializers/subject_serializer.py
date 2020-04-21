from rest_framework import serializers

from backend.models import Subject
from . import FinalSerializer
from .filterable_model_list_serializer import FilterableModelListSerializer


class SubjectsListSerializer(FilterableModelListSerializer):
    MODEL = Subject

    def to_representation(self, data):
        data = data.filter(**self._filter_params(self.context["filters"])).distinct()
        return super(SubjectsListSerializer, self).to_representation(data)


class SubjectSerializer(serializers.ModelSerializer):
    finals = FinalSerializer(source='final_set', many=True)

    class Meta:
        model = Subject
        list_serializer_class = SubjectsListSerializer
        fields = ('id', 'name', 'finals')
