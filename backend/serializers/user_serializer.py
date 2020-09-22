from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from backend.interactors.image_validator_interactor import ImageValidatorInteractor


class UserCustomCreateSerializer(UserCreateSerializer):
    def create(self, validated_data):
        b64_string = self.context['request']['image']
        validation_result = ImageValidatorInteractor(b64_string).validate_image()
        if validation_result.errors:
            raise serializers.ValidationError(validation_result.errors)
        validated_data['face_encodings'] = validation_result.data
        return super().create(validated_data)
