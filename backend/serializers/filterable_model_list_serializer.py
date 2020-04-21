from rest_framework import serializers
from django.db import models


class FilterableModelListSerializer(serializers.ListSerializer):
    MODEL = models.Model

    def _filter_params(self, filter_params):
        return dict({self.MODEL.ALLOWED_FILTERS[key]: value for key, value in filter_params.items() if key in self.MODEL.ALLOWED_FILTERS})
