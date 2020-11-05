from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.serializers.user_serializer import UserCustomCreateSerializer
from ..interactors.image_validator_interactor import ImageValidatorInteractor
from ..models import User
from ..permissions import IsStudent


class UserCustomViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserCustomCreateSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_serializer_class(self):
        return UserCustomCreateSerializer

    @action(detail=False, methods=['POST'])
    def is_me(self, request):
        result = ImageValidatorInteractor(request.data['photo']).validate_identity(request.user.student)
        return Response({"match": result}, status=status.HTTP_200_OK)
