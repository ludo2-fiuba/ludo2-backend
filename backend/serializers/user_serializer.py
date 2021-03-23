from djoser.serializers import UserCreateSerializer, User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from backend.api_exceptions import InvalidImageError
from backend.models import User
from backend.services.auth_fiuba_service import AuthFiubaService
from backend.services.image_validator_service import ImageValidatorService


class UserCustomCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('code', 'is_student', 'is_teacher')

    def create(self, validated_data):
        b64_string = self.context['request'].data['image']
        try:
            face_encodings = ImageValidatorService(b64_string).validate_image()
        except InvalidImageError as e:
            raise serializers.ValidationError(e.detail)
        validated_data['face_encodings'] = face_encodings
        return super().create(validated_data)

    def validate(self, attrs):
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'code'

    class Meta:
        model = User
        fields = ('code',)

    def validate(self, attrs):
        token_response = self.fiuba_service().get_token(self.context['request'].data['code'])

        user_info = self.fiuba_service().userinfo(token_response['access_token'])

        user = User.objects.get(dni=user_info['sub'])

        data = {}

        refresh = self.get_token(user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        self._validated_data = data

        return data

    def is_valid(self, raise_exception=False):
        return self.validate(self.initial_data)

    def fiuba_service(self):
        return AuthFiubaService()
