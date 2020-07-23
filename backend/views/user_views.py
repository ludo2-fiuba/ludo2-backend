from djoser.views import UserViewSet

from backend.serializers.user_serializer import UserCustomCreateSerializer
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
