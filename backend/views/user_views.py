from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.serializers.user_serializer import UserCustomCreateSerializer
from ..interactors.final_requirements_validator_interactor import IdentityValidatorInteractor
from ..models import User


class UserCustomViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserCustomCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['image'] = self.request.data['image']
        return context

    def get_serializer_class(self):
        return UserCustomCreateSerializer

    @action(detail=False, methods=['POST'])
    def is_me(self, request):
        result = IdentityValidatorInteractor(request.user, request.data['photo']).validate()
        match = not bool(result.errors)
        return Response({"match": match}, status=status.HTTP_200_OK)
