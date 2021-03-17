from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from backend.api_exceptions import InvalidImageError
from backend.models import User
from backend.services.image_validator_service import ImageValidatorService


class UserCustomCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('dni', 'email', 'is_student', 'is_teacher')

    def create(self, validated_data):
        b64_string = self.context['request'].data['image']
        try:
            face_encodings = ImageValidatorService(b64_string).validate_image()
        except InvalidImageError as e:
            raise serializers.ValidationError(e.detail)
        validated_data['face_encodings'] = face_encodings
        return super().create(validated_data)

    def validate(self, attrs):
        return attrs;
