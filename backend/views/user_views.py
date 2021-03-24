from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.views import TokenObtainPairView

from backend.serializers.user_serializer import UserCustomCreateSerializer, CustomTokenObtainPairSerializer
from backend.services.image_validator_service import ImageValidatorService
from ..models import User


class UserCustomViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserCustomCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return UserCustomCreateSerializer

    @action(detail=False, methods=['POST'])
    def is_me(self, request):
        result = ImageValidatorService(request.data['image']).validate_identity(request.user.student)
        return Response({"match": result}, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = CustomTokenObtainPairSerializer

    www_authenticate_realm = 'api'

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class TokenError(Exception):
    pass


class InvalidToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    # default_detail = _('Token is invalid or expired')
    default_code = 'token_not_valid'


token_obtain_pair = CustomTokenObtainPairView.as_view()
