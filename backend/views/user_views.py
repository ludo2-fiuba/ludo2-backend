from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def get_serializer_class(self):
        return CustomTokenObtainPairSerializer

token_obtain_pair = CustomTokenObtainPairView.as_view()
