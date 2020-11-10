from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from backend.api_exceptions import InvalidImageError
from backend.services.image_validator_service import ImageValidatorService


class UserCustomCreateSerializer(UserCreateSerializer):
    def create(self, validated_data):
        b64_string = self.context['request'].data['image']
        try:
            face_encodings = ImageValidatorService(b64_string).validate_image()
        except InvalidImageError as e:
            raise serializers.ValidationError(e.detail)
        validated_data['face_encodings'] = face_encodings
        return super().create(validated_data)
