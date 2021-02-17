from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.serializers.user_serializer import UserCustomCreateSerializer
from backend.services.image_validator_service import ImageValidatorService
from ..models import User
from ..services.siu_service import SiuService


class UserCustomViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserCustomCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return UserCustomCreateSerializer

    @action(detail=False, methods=['POST'])
    def is_me(self, request):
        result = ImageValidatorService(request.data['photo']).validate_identity(request.user.student)
        return Response({"match": result}, status=status.HTTP_200_OK)

    def _get_siu_user(self, is_student, email, dni):
            return SiuService().get_student(email, dni) if is_student else SiuService().get_teacher(email, dni)
