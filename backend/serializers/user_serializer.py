from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from backend.api_exceptions import InvalidImageError
from backend.interactors.image_validator_interactor import ImageValidatorInteractor


class UserCustomCreateSerializer(UserCreateSerializer):
    def create(self, validated_data):
        b64_string = self.context['request'].data['image']
        try:
            validation_result = ImageValidatorInteractor(b64_string).validate_image()
        except InvalidImageError as e:
            raise serializers.ValidationError(e.detail)
        validated_data['face_encodings'] = validation_result.data
        return super().create(validated_data)
