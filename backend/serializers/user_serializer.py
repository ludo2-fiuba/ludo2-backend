from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from backend.api_exceptions import InvalidImageError
from backend.models import User
from backend.services.image_validator_service import ImageValidatorService
from backend.services.siu_service import SiuService


class UserCustomCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('dni', 'email', 'is_student', 'is_teacher')

    def create(self, validated_data):
        b64_string = self.context['request'].data['image']

        face_encodings = self._get_face_encodings(b64_string)
        siu_user = self._get_siu_user(validated_data['is_student'], validated_data['email'], validated_data['dni'])

        validated_data['face_encodings'] = face_encodings
        validated_data['first_name'] = siu_user['first_name']
        validated_data['last_name'] = siu_user['last_name']
        validated_data['file'] = siu_user['file']

        return super().create(validated_data)

    def validate(self, attrs):
        return attrs

    def _get_face_encodings(self, b64_string):
        try:
            return ImageValidatorService(b64_string).validate_image()
        except InvalidImageError as e:
            raise serializers.ValidationError(e.detail)

    def _get_siu_user(self, is_student, email, dni):
            return SiuService().get_student(email, dni) if is_student else SiuService().get_teacher(email, dni)
